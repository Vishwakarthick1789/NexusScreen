import logging
import PyPDF2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Robustly extracts text from a PDF file using PyPDF2.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if reader.is_encrypted:
                logger.warning(f"PDF is password protected: {pdf_path}")
                return ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        logger.error(f"Error parsing PDF '{pdf_path}': {e}")
        return ""
        
    return text.strip()
