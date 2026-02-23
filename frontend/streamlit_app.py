import sys
import os
import matplotlib.pyplot as plt

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from app.services.recommender import calculate_keyword_coverage
from app.services.parser import parse_resume
from app.services.skill_extractor import load_skills, extract_skills_from_text
from app.services.similarity import calculate_similarity
from app.services.recommender import (
    get_missing_skills,
    get_matching_skills,
    generate_feedback
)

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.markdown(
    """
    <style>
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("🚀 AI-Powered Resume Analyzer")

# Upload Resume
uploaded_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])

# Job Description
job_description = st.text_area("Paste Job Description Here")

if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        # Save uploaded file temporarily
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
        keyword_score = calculate_keyword_coverage(resume_skills, jd_skills)
        st.info(f"Detected {len(resume_skills)} skills in your resume.")
        # Similarity using skills only
        resume_text_for_similarity = " ".join(resume_skills)
        jd_text_for_similarity = " ".join(jd_skills)

        match_score = calculate_similarity(
            resume_text_for_similarity,
            jd_text_for_similarity
        )

        missing_skills = get_missing_skills(resume_skills, jd_skills)
        matching_skills = get_matching_skills(resume_skills, jd_skills)
        st.subheader("📈 Skill Comparison Chart")

        labels = ["Matching Skills", "Missing Skills"]
        values = [len(matching_skills), len(missing_skills)]

        fig = plt.figure()
        plt.bar(labels, values)
        plt.xlabel("Skill Category")
        plt.ylabel("Number of Skills")

        st.pyplot(fig)
        feedback = generate_feedback(match_score, missing_skills)

    # Display Results
    st.subheader("📊 Match Score")
    st.progress(int(match_score))

    if match_score > 70:
        st.success(f"Excellent Match — {match_score}%")
    elif match_score > 40:
        st.warning(f"Moderate Match — {match_score}%")
    else:
        st.error(f"Low Match — {match_score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matching Skills")
        st.write(matching_skills)

    with col2:
        st.subheader("❌ Missing Skills")
        for skill in matching_skills:
            st.markdown(f"🟢 **{skill.upper()}**")

        for skill in missing_skills:
            st.markdown(f"🔴 **{skill.upper()}**")

        st.subheader("💡 Feedback")
        st.write(feedback)
    st.subheader("📊 ATS Keyword Coverage")

    st.progress(int(keyword_score))

    if keyword_score > 70:
        st.success(f"Strong ATS Match — {keyword_score}% keywords covered")
    elif keyword_score > 40:
        st.warning(f"Moderate ATS Match — {keyword_score}% keywords covered")
    else:
        st.error(f"Low ATS Match — {keyword_score}% keywords covered")
        

else:
    st.warning("Please upload resume and paste job description.")
