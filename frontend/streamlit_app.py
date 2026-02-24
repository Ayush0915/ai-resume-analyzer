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
from app.services.signal_noise_analyzer import analyze_signal_to_noise

st.set_page_config(page_title="AI Resume Intelligence Platform", layout="wide")

st.title("🚀 AI Resume Intelligence Platform")

uploaded_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description Here")


if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        # ==========================
        # SAVE FILE
        # ==========================
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # ==========================
        # PARSE RESUME
        # ==========================
        result = parse_resume(file_path)

        # ⚠ IMPORTANT:
        # Use raw text for similarity (preserve punctuation for sentence splitting)
        resume_text_raw = result["raw_text"]
        resume_text_clean = result["clean_text"]

        # ==========================
        # SKILL EXTRACTION
        # ==========================
        skills_list = load_skills()

        resume_skills = extract_skills_from_text(resume_text_clean, skills_list)
        jd_skills = extract_skills_from_text(job_description, skills_list)

        # ==========================
        # ATS KEYWORD COVERAGE
        # ==========================
        keyword_score = calculate_keyword_coverage(resume_skills, jd_skills)

        # ==========================
        # SEMANTIC SIMILARITY (Sentence-Level)
        # ==========================
        similarity_result = calculate_similarity(
            resume_text_raw,
            job_description
        )

        match_score = similarity_result["final_score"]
        top_matches = similarity_result["top_matches"]

        # ==========================
        # SKILL GAP ANALYSIS (Dynamic)
        # ==========================
        missing_skills = get_missing_skills(resume_skills, jd_skills)
        matching_skills = get_matching_skills(resume_skills, jd_skills)

        gap_analysis = classify_skill_gaps(
            missing_skills,
            jd_skills,
            job_description
        )
        signal_result = analyze_signal_to_noise(resume_text_raw)

        # ==========================
        # FEEDBACK
        # ==========================
        feedback = generate_feedback(match_score, missing_skills)

        # ==========================
        # DISPLAY SECTION
        # ==========================

        st.info(f"Detected {len(resume_skills)} skills in your resume.")

        # --------------------------
        # MATCH SCORE
        # --------------------------
        st.subheader("📊 Semantic Match Score")
        st.progress(int(match_score))

        if match_score >= 75:
            st.success(f"Strong Alignment — {match_score}%")
        elif match_score >= 50:
            st.warning(f"Moderate Alignment — {match_score}%")
        else:
            st.error(f"Low Alignment — {match_score}%")

        # 🔍 Top Matching Sentences
        st.subheader("🔍 Top Matching Resume Segments")

        if top_matches:
            for sentence, score in top_matches:
                st.markdown(f"**{score}%** — {sentence}")
        else:
            st.info("No strong semantic matches detected.")

        # --------------------------
        # ATS SCORE
        # --------------------------
        st.subheader("📊 ATS Keyword Coverage")
        st.progress(int(keyword_score))

        if keyword_score >= 75:
            st.success(f"Strong ATS Match — {keyword_score}% keywords covered")
        elif keyword_score >= 50:
            st.warning(f"Moderate ATS Match — {keyword_score}% keywords covered")
        else:
            st.error(f"Low ATS Match — {keyword_score}% keywords covered")

        # --------------------------
        # SKILL SUMMARY
        # --------------------------
        st.subheader("📊 Skill Summary")

        col1, col2 = st.columns(2)
        col1.metric("✅ Matching Skills", len(matching_skills))
        col2.metric("❌ Missing Skills", len(missing_skills))

        # --------------------------
        # SKILL LISTS
        # --------------------------
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

        # --------------------------
        # FEEDBACK
        # --------------------------
        st.subheader("💡 Intelligent Feedback")
        st.info(feedback)
        st.subheader("🧠 Resume Signal-to-Noise Analysis")

        st.metric("Resume Clarity Score", f"{signal_result['clarity_score']}/100")

        if signal_result["weak_phrases_found"]:
            st.warning("⚠ Weak Phrases Detected:")
            for phrase in signal_result["weak_phrases_found"]:
                st.markdown(f"- {phrase}")

        if signal_result["strong_verbs_found"]:
            st.success("💪 Strong Action Verbs Used:")
            for verb in signal_result["strong_verbs_found"]:
                st.markdown(f"- {verb}")

        st.info(f"📊 Quantified Achievements Detected: {signal_result['quantified_sentences']}")

    else:
        st.warning("Please upload resume and paste job description.")