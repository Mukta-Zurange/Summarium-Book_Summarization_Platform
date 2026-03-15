import re
import os
import fitz
from transformers import BartTokenizer

def preprocess_text(text):
    text = re.sub(r'[\n\t\r]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'([.!?,:;"\'(){}[\]])\s*(\1){1,}', r'\1', text)
    text = text.replace("®", "")
    return text.strip()

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def smart_chunk_text(text, tokenizer,
                     target_chunks=8,
                     min_chunk_tokens=400,
                     max_chunk_tokens=700,
                     overlap_ratio=0.2):

    input_ids = tokenizer.encode(text)
    total_tokens = len(input_ids)

    approx_chunk_size = total_tokens // target_chunks
    chunk_size = max(min_chunk_tokens, min(approx_chunk_size, max_chunk_tokens))

    overlap = int(chunk_size * overlap_ratio)
    step = chunk_size - overlap

    chunks = []
    i = 0

    while i < total_tokens:
        chunk_ids = input_ids[i:i + chunk_size]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)
        i += step

    return chunks
