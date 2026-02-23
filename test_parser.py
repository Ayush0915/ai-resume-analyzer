from app.services.parser import parse_resume
from app.services.skill_extractor import load_skills, extract_skills_from_text
from app.services.similarity import calculate_similarity
from app.services.recommender import (
    get_missing_skills,
    get_matching_skills,
    generate_feedback
)

# STEP 1 — Parse Resume
file_path = "data/sample_resume.pdf"
result = parse_resume(file_path)
resume_text = result["clean_text"]

# STEP 2 — Load skills database
skills_list = load_skills()

# STEP 3 — Extract skills
resume_skills = extract_skills_from_text(resume_text, skills_list)

# STEP 4 — Sample Job Description
job_description = """
We are looking for a Data Scientist with strong skills in Python,
Machine Learning, Pandas, NumPy, SQL, Docker, and AWS.
"""

jd_skills = extract_skills_from_text(job_description, skills_list)

# STEP 5 — Compare skills only (better method)
resume_text_for_similarity = " ".join(resume_skills)
jd_text_for_similarity = " ".join(jd_skills)

match_score = calculate_similarity(
    resume_text_for_similarity,
    jd_text_for_similarity
)

# STEP 6 — Get insights
missing_skills = get_missing_skills(resume_skills, jd_skills)
matching_skills = get_matching_skills(resume_skills, jd_skills)

feedback = generate_feedback(match_score, missing_skills)

# OUTPUT
print("\n===== MATCH SCORE =====")
print(f"{match_score}%")

print("\n===== MATCHING SKILLS =====")
print(matching_skills)

print("\n===== MISSING SKILLS =====")
print(missing_skills)

print("\n===== FEEDBACK =====")
print(feedback)