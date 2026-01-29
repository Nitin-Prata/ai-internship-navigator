import fitz  
import docx


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF resume
    """
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract text from DOCX resume
    """
    document = docx.Document(file_bytes)
    text = "\n".join([para.text for para in document.paragraphs])
    return text.strip()


def parse_resume(file_bytes: bytes, filename: str) -> str:
    """
    Detect file type and extract text
    """
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format")
