import requests
import os
from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file using pypdf."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No file at {file_path}")
    try:
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        logger.info("PDF text extraction successful")
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}", exc_info=True)
        return ""

def extract_text_from_url(url: str) -> str:
    """Fetches and returns sample text from the given URL."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch from URL: {url}")
        logger.info(f"Successfully fetched data from URL: {url}")
        return response.text[:2000]  # Trimmed sample
    except Exception as e:
        logger.error(f"Error fetching from URL: {str(e)}", exc_info=True)
        return ""

def get_base_paper_text(source: str, is_url=False, max_length: int = 4000) -> str:
    """Returns base paper text from a file path or URL, trimmed and cleaned."""
    text = extract_text_from_url(source) if is_url else extract_text_from_pdf(source)
    text = ' '.join(text.split())  # Clean extra whitespace
    return text[:max_length]
