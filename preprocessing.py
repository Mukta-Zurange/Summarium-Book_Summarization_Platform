import re

def preprocess_text(text: str) -> str:
    # Remove page numbers (e.g. "12", "- 12 -", "Page 12")
    text = re.sub(r'\bPage\s+\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b\d+\b', '', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)

    # Fix multiple punctuations (e.g. "..." or ",,," or "!!")
    text = re.sub(r'([.!?,;:]){2,}', r'\1', text)

    # Remove newlines, tabs
    text = re.sub(r'[\n\t\r]+', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()