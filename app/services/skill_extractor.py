import pandas as pd


def load_skills(file_path: str = "skills_database.csv") -> list:
    """Load skills from CSV file"""
    df = pd.read_csv(file_path)
    skills = df["skill"].dropna().tolist()
    return [skill.lower() for skill in skills]


def extract_skills_from_text(text: str, skills_list: list) -> list:
    """Extract matching skills from resume text"""

    if not text:
        return []

    detected_skills = []

    text = text.lower()

    for skill in skills_list:
        if skill in text:
            detected_skills.append(skill)

    return list(set(detected_skills))  # remove duplicates