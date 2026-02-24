# 🚀 AI Resume Intelligence Platform

A Transformer-powered Resume Intelligence System that evaluates resumes against job descriptions using semantic similarity, skill gap analysis, and writing quality assessment.

Built for placement preparation, ATS optimization, and resume performance analysis.

---

## 🧠 Project Overview

This system goes beyond basic keyword matching.

It performs:

- 🔍 Sentence-level semantic alignment using Transformer embeddings
- 🧠 Intelligent skill extraction with regex + synonym normalization
- 📊 Dynamic skill gap severity classification
- 📈 ATS keyword coverage analysis
- 🧾 Resume Signal-to-Noise (writing quality) evaluation
- 💡 Actionable improvement suggestions

---

## 🔥 Core Features

### 📄 1. Resume Parsing
- Supports PDF & DOCX
- Cleans and preprocesses text
- Separates raw and cleaned content for different NLP tasks

---

### 🤖 2. Semantic Similarity Engine (Transformer-Based)

- Uses `all-MiniLM-L6-v2` (BERT-derived Sentence Transformer)
- Sentence-level embedding comparison
- Filters out irrelevant sections (contact info, education)
- Returns:
  - Semantic Match Score
  - Top Matching Resume Segments

This provides explainable AI alignment instead of simple keyword overlap.

---

### 🧠 3. Intelligent Skill Extraction

- Regex word-boundary matching
- Synonym normalization (ML → Machine Learning, etc.)
- Avoids false positives (e.g., SQL ≠ MySQL)
- Extracts:
  - Resume Skills
  - JD Skills
  - Matching Skills
  - Missing Skills

---

### 🎯 4. Dynamic Skill Gap Severity

Skill gaps are classified dynamically based on JD frequency:

- 🔴 Critical
- 🟡 Important
- 🟢 Optional

No hardcoded assumptions.

---

### 📊 5. ATS Keyword Coverage

Computes percentage of JD skills covered in resume.

Simulates Applicant Tracking System keyword analysis.

---

### 🧠 6. Resume Signal-to-Noise Analysis (Writing Quality Engine)

Analyzes only Project/Experience sections.

Detects:

- ⚠ Weak phrases (e.g., "worked on", "responsible for")
- 💪 Strong action verbs (developed, engineered, built)
- 📈 Quantified achievements (%, numbers, impact metrics)

Generates:

- Resume Clarity Score (0–100)
- Writing quality diagnostics

This differentiates the system from typical resume analyzers.

---


---

## 🛠️ Tech Stack

- Python
- Streamlit
- Sentence Transformers (BERT-derived MiniLM)
- scikit-learn
- Pandas
- NumPy
- NLTK
- PyPDF2
- python-docx

---

## ⚙️ Installation

```bash
git clone https://github.com/Ayush0915/ai-resume-analyzer.git
cd ai-resume-analyzer
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py