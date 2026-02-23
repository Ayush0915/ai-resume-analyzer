import sys
import os
import pandas as pd
import streamlit as st

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.recommender import (
    calculate_keyword_coverage,
    get_missing_skills,
    get_matching_skills,
    generate_feedback
)
from app.services.parser import parse_resume
from app.services.skill_extractor import load_skills, extract_skills_from_text
from app.services.similarity import calculate_similarity


st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI-Powered Resume Analyzer")

uploaded_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description Here")

if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Parse resume
        result = parse_resume(file_path)
        resume_text = result["clean_text"]

        # Load skills
        skills_list = load_skills()

        # Extract skills
        resume_skills = extract_skills_from_text(resume_text, skills_list)
        jd_skills = extract_skills_from_text(job_description, skills_list)

        # Scores
        keyword_score = calculate_keyword_coverage(resume_skills, jd_skills)

        resume_text_for_similarity = " ".join(resume_skills)
        jd_text_for_similarity = " ".join(jd_skills)

        match_score = calculate_similarity(
            resume_text_for_similarity,
            jd_text_for_similarity
        )

        missing_skills = get_missing_skills(resume_skills, jd_skills)
        matching_skills = get_matching_skills(resume_skills, jd_skills)

        feedback = generate_feedback(match_score, missing_skills)

        # ==========================
        # DISPLAY SECTION
        # ==========================

        st.info(f"Detected {len(resume_skills)} skills in your resume.")

        st.subheader("📊 Match Score")
        st.progress(int(match_score))

        if match_score > 70:
            st.success(f"Excellent Match — {match_score}%")
        elif match_score > 40:
            st.warning(f"Moderate Match — {match_score}%")
        else:
            st.error(f"Low Match — {match_score}%")

        st.subheader("📊 ATS Keyword Coverage")
        st.progress(int(keyword_score))

        if keyword_score > 70:
            st.success(f"Strong ATS Match — {keyword_score}% keywords covered")
        elif keyword_score > 40:
            st.warning(f"Moderate ATS Match — {keyword_score}% keywords covered")
        else:
            st.error(f"Low ATS Match — {keyword_score}% keywords covered")

        # Metrics Layout
        st.subheader("📊 Skill Summary")
        col1, col2 = st.columns(2)

        col1.metric("✅ Matching Skills", len(matching_skills))
        col2.metric("❌ Missing Skills", len(missing_skills))

        # Clean Streamlit Bar Chart
        chart_data = pd.DataFrame({
            "Category": ["Matching Skills", "Missing Skills"],
            "Count": [len(matching_skills), len(missing_skills)]
        })

        st.bar_chart(chart_data.set_index("Category"))

        # Skill Lists
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matching Skills")
            st.write(matching_skills)

        with col2:
            st.subheader("❌ Missing Skills")
            st.write(missing_skills)

        st.subheader("💡 Feedback")
        st.write(feedback)

    else:
        st.warning("Please upload resume and paste job description.")