import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()

    doc.close()
    return text


def extract_text(file_path: str) -> str:
    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".pdf":
        return extract_text_from_pdf(file_path)

    elif ext.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Only PDF and TXT supported")