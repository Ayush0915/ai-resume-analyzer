from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculate semantic similarity using BERT embeddings
    Returns percentage score
    """

    if not resume_text or not jd_text:
        return 0.0

    # Generate embeddings
    resume_embedding = model.encode(resume_text)
    jd_embedding = model.encode(jd_text)

    # Reshape for cosine similarity
    resume_embedding = np.array(resume_embedding).reshape(1, -1)
    jd_embedding = np.array(jd_embedding).reshape(1, -1)

    similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]

    score = round(float(similarity) * 100, 2)

    return score