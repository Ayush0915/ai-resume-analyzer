import os
from PyPDF2 import PdfReader
import docx
from app.utils.text_cleaner import clean_text


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF resume"""
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX resume"""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text


def parse_resume(file_path: str) -> dict:
    """Main resume parsing function"""

    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file format")

    cleaned = clean_text(raw_text)

    return {
        "raw_text": raw_text,
        "clean_text": cleaned
    }