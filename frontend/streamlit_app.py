import sys
import os
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
from app.services.skill_gap_analyzer import classify_skill_gaps


st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI-Powered Resume Analyzer")

uploaded_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description Here")


if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        # Save uploaded file
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

        gap_analysis = classify_skill_gaps(missing_skills, jd_skills)

        feedback = generate_feedback(match_score, missing_skills)

        # ==========================
        # DISPLAY SECTION
        # ==========================

        st.info(f"Detected {len(resume_skills)} skills in your resume.")

        # Match Score
        st.subheader("📊 Match Score")
        st.progress(int(match_score))

        if match_score > 70:
            st.success(f"Excellent Match — {match_score}%")
        elif match_score > 40:
            st.warning(f"Moderate Match — {match_score}%")
        else:
            st.error(f"Low Match — {match_score}%")

        # ATS Score
        st.subheader("📊 ATS Keyword Coverage")
        st.progress(int(keyword_score))

        if keyword_score > 70:
            st.success(f"Strong ATS Match — {keyword_score}% keywords covered")
        elif keyword_score > 40:
            st.warning(f"Moderate ATS Match — {keyword_score}% keywords covered")
        else:
            st.error(f"Low ATS Match — {keyword_score}% keywords covered")

        # Skill Summary Metrics
        st.subheader("📊 Skill Summary")
        col1, col2 = st.columns(2)

        col1.metric("✅ Matching Skills", len(matching_skills))
        col2.metric("❌ Missing Skills", len(missing_skills))

        # Skill Lists
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matching Skills")
            for skill in matching_skills:
                st.success(skill.upper())

        with col2:
            st.subheader("🎯 Skill Gap Severity Analysis")

            if gap_analysis["critical"]:
                st.error("🔴 Critical Skills Missing")
                for skill in gap_analysis["critical"]:
                    st.markdown(f"- **{skill.upper()}**")

            if gap_analysis["important"]:
                st.warning("🟡 Important Skills Missing")
                for skill in gap_analysis["important"]:
                    st.markdown(f"- {skill.upper()}")

            if gap_analysis["optional"]:
                st.info("🟢 Optional Skills Missing")
                for skill in gap_analysis["optional"]:
                    st.markdown(f"- {skill.upper()}")

        # Feedback (Only Once)
        st.subheader("💡 Feedback")
        st.info(feedback)

    else:
        st.warning("Please upload resume and paste job description.")