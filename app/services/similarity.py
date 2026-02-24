from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
import re

# Download once (only first run)
nltk.download("punkt")

# Load model once globally
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text: str, jd_text: str, top_k: int = 5):
    """
    Sentence-level semantic similarity with intelligent filtering.

    Returns:
        {
            "final_score": float,
            "top_matches": list of (sentence, score)
        }
    """

    if not resume_text or not jd_text:
        return {
            "final_score": 0.0,
            "top_matches": []
        }

    # -----------------------------
    # Sentence Tokenization
    # -----------------------------
    sentences = nltk.sent_tokenize(resume_text)

    # -----------------------------
    # Filter Irrelevant Sentences
    # -----------------------------
    filtered_sentences = []

    for sentence in sentences:
        s = sentence.lower()

        # Remove contact info / links
        if re.search(r'\b(email|phone|linkedin|github|leet|hackerrank)\b', s):
            continue

        # Remove very short sentences
        if len(sentence.split()) < 6:
            continue

        # Remove education-only lines
        if re.search(r'\b(bachelor|school|education|cgpa|percent)\b', s):
            continue

        filtered_sentences.append(sentence)

    # If filtering removes everything, fallback to original
    if not filtered_sentences:
        filtered_sentences = sentences

    # -----------------------------
    # Generate Embeddings
    # -----------------------------
    jd_embedding = model.encode([jd_text])
    sentence_embeddings = model.encode(filtered_sentences)

    # -----------------------------
    # Compute Similarity
    # -----------------------------
    similarities = cosine_similarity(sentence_embeddings, jd_embedding).flatten()

    # Pair sentences with scores
    sentence_scores = list(zip(filtered_sentences, similarities))

    # Sort descending
    sentence_scores = sorted(sentence_scores, key=lambda x: x[1], reverse=True)

    # Take top_k
    top_matches = sentence_scores[:top_k]

    # Compute final score as average of top_k
    if top_matches:
        top_scores = [score for _, score in top_matches]
        final_score = np.mean(top_scores)
    else:
        final_score = 0.0

    return {
        "final_score": round(float(final_score) * 100, 2),
        "top_matches": [
            (sent, round(float(score) * 100, 2))
            for sent, score in top_matches
        ]
    }