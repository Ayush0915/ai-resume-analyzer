import re
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
WEAK_PHRASES = [
    "responsible for",
    "worked on",
    "helped with",
    "assisted in",
    "involved in"
]

STRONG_VERBS = [
    "developed",
    "engineered",
    "implemented",
    "optimized",
    "designed",
    "built",
    "created",
    "led",
    "improved"
]


def extract_relevant_sections(text: str):
    """
    Extract only project / experience sections.
    Heuristic-based section filtering.
    """

    lines = text.split("\n")
    capture = False
    collected = []

    for line in lines:
        lower = line.lower()

        # Start capturing when relevant section appears
        if any(keyword in lower for keyword in ["experience", "project", "internship", "work"]):
            capture = True
            continue

        # Stop capturing at education section
        if "education" in lower:
            capture = False

        if capture:
            collected.append(line)

    return " ".join(collected)


def analyze_signal_to_noise(resume_text: str):

    relevant_text = extract_relevant_sections(resume_text)

    sentences = nltk.sent_tokenize(relevant_text)

    if not sentences:
        return {
            "clarity_score": 0,
            "weak_phrases_found": [],
            "strong_verbs_found": [],
            "quantified_sentences": 0
        }

    weak_count = 0
    strong_count = 0
    quantified_count = 0

    weak_found = []
    strong_found = []

    for sentence in sentences:
        s = sentence.lower()

        # Weak phrase detection
        for phrase in WEAK_PHRASES:
            if phrase in s:
                weak_count += 1
                weak_found.append(phrase)

        # Strong verb detection
        for verb in STRONG_VERBS:
            if re.search(r'\b' + verb + r'\b', s):
                strong_count += 1
                strong_found.append(verb)

        # Quantification detection
        if re.search(r'\d+%|\d+\+|\$\d+|\d+\s?(users|clients|logs|projects|models|apps)', s):
            quantified_count += 1

    # -----------------------------
    # PROPORTIONAL SCORING LOGIC
    # -----------------------------
    total_sentences = len(sentences)

    weak_ratio = weak_count / total_sentences
    strong_ratio = strong_count / total_sentences
    quant_ratio = quantified_count / total_sentences

    clarity_score = (
        60                        # base score
        - (weak_ratio * 40)       # heavy penalty
        + (strong_ratio * 25)     # moderate reward
        + (quant_ratio * 25)      # moderate reward
    )

    clarity_score = max(0, min(100, round(clarity_score, 2)))

    return {
        "clarity_score": clarity_score,
        "weak_phrases_found": list(set(weak_found)),
        "strong_verbs_found": list(set(strong_found)),
        "quantified_sentences": quantified_count
    }