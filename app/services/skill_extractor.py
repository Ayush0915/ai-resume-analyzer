import pandas as pd
import re

# Synonym dictionary
SYNONYMS = {
    "ml": "machine learning",
    "dl": "deep learning",
    "js": "javascript",
    "py": "python",
    "tf": "tensorflow",
    "np": "numpy",
    "nlp": "natural language processing"
}


def load_skills(file_path: str = "skills_database.csv") -> list:
    df = pd.read_csv(file_path)
    skills = df["skill"].dropna().tolist()
    return [skill.lower().strip() for skill in skills]


def normalize_text(text: str) -> str:
    text = text.lower()

    for short, full in SYNONYMS.items():
        pattern = r'\b' + re.escape(short) + r'\b'
        text = re.sub(pattern, full, text)

    return text


def extract_skills_from_text(text: str, skills_list: list) -> list:

    if not text:
        return []

    text = normalize_text(text)

    detected_skills = []

    for skill in skills_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            detected_skills.append(skill)

    return sorted(list(set(detected_skills)))