
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from preprocessing import preprocess_text


def chunk_text(text: str, chunk_size: int = 8000, overlap: int = 0):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap if overlap > 0 else end
    return chunks


def clean_output(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = re.sub(r'#{1,6}\s+', '', text)
    text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()



def get_paragraph_instruction(total_words: int, length: str) -> str:
    if length == "short":
        return "Write the summary in 1 short paragraph only."
    elif length == "medium":
        if total_words < 8000:
            return "Write the summary in 2 paragraphs."
        else:
            return "Write the summary in 2 to 3 paragraphs."
    else:  # detailed
        if total_words < 8000:
            return "Write the summary in 3 paragraphs."
        else:
            return "Write the summary in 4 to 5 paragraphs."


def summarize_text(full_text: str, format: str = "paragraph", length: str = "medium", progress_callback=None, existing_chunks: list = None) -> tuple:
    import time

    # If no existing chunks, process the text
    if existing_chunks:
        chunk_summaries = existing_chunks
        print(f"Reusing {len(chunk_summaries)} existing chunk summaries")
        if progress_callback:
            progress_callback(80)
    else:
        text = preprocess_text(full_text)
        total_words = len(text.split())
        chunks = chunk_text(text, chunk_size=8000)
        total_chunks = len(chunks)
        print(f"Total words: {total_words}, Chunks: {total_chunks}")

        chunk_summaries = [None] * total_chunks
        completed = [0]

        def call_api(i, chunk):
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{
                    "role": "user",
                    "content": (
                        "Summarize the following text briefly and to the point. "
                        "Only include the most important information. "
                        "Do NOT copy sentences from the text. "
                        "Do not add any extra explanation or padding.\n\n"
                        f"{chunk}"
                    )
                }]
            )
            return i, response.choices[0].message.content

        for i, chunk in enumerate(chunks):
            while True:
                try:
                    _, summary = call_api(i, chunk)
                    chunk_summaries[i] = summary
                    completed[0] += 1
                    if progress_callback:
                        pct = int((completed[0] / total_chunks) * 80)
                        progress_callback(pct)
                    break
                except Exception as e:
                    if "rate_limit" in str(e).lower() or "429" in str(e) or "413" in str(e):
                        print(f"Rate limit hit, waiting 10s...")
                        time.sleep(10)
                    else:
                        raise e

    combined = " ".join(chunk_summaries)

    if progress_callback:
        progress_callback(85)

    total_words = len(combined.split())

    if format == "bullet":
        format_instruction = (
            "Write the summary as bullet points. "
            "Each bullet point should start with a dash (-). "
        )
        if length == "short":
            format_instruction += "Include only 4-5 bullet points."
        elif length == "medium":
            format_instruction += "Include 6-8 bullet points."
        else:
            format_instruction += "Include 10-12 detailed bullet points."
    else:
        format_instruction = get_paragraph_instruction(total_words, length)

    if len(combined) > 4000:
        combined = combined[:4000]

    while True:
        try:
            final = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{
                    "role": "user",
                    "content": (
                        f"Combine these section summaries into one final summary. "
                        f"{format_instruction} "
                        "Do not repeat points. "
                        "Do not mention word count or any numbers. "
                        "Do not start with phrases like 'Here is a summary'. "
                        "Just write the summary directly. "
                        "Use proper punctuation and grammar.\n\n"
                        f"{combined}"
                    )
                }]
            )
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e) or "413" in str(e):
                print(f"Rate limit on final call, waiting 15s...")
                time.sleep(15)
            else:
                raise e

    if progress_callback:
        progress_callback(100)

    result = clean_output(final.choices[0].message.content)

    if format == "bullet":
        lines = result.split("\n")
        cleaned = []
        for line in lines:
            line = line.strip()
            if line:
                if not line.startswith("-"):
                    line = "- " + line
                cleaned.append(line)
        result = "\n".join(cleaned)

    # Return result AND chunk_summaries so they can be saved
    return result, chunk_summaries

def generate_mindmap_data(summary_text: str) -> dict:
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": (
                "Analyze the following summary and create the most appropriate mind map structure for it.\n\n"
                "First, decide what type of content this is. It could be:\n"
                "- A step by step process or tutorial\n"
                "- A hierarchical classification or taxonomy\n"
                "- A comparison of things\n"
                "- A cause and effect relationship\n"
                "- A timeline of events\n"
                "- General concepts and topics\n"
                "- Or any other structure that fits best\n\n"
                "Then create a mind map JSON that best represents this content using the most suitable structure.\n\n"
                "Return a JSON object with this format:\n"
                "{\n"
                '  "name": "<central topic>",\n'
                '  "type": "<what type of content this is in 2-3 words>",\n'
                '  "children": [\n'
                '    { "name": "<main point>", "children": [\n'
                '      { "name": "<detail>" },\n'
                '      { "name": "<detail>" }\n'
                "    ]}\n"
                "  ]\n"
                "}\n\n"
                "Rules:\n"
                "- Choose node names that reflect the actual content type\n"
                "- For steps use 'Step 1: ...' format\n"
                "- For timeline use dates or periods as node names\n"
                "- For comparison use the items being compared as main nodes\n"
                "- For cause/effect use 'Cause:' and 'Effect:' prefixes\n"
                "- Include ONLY 3-4 main nodes\n"
                "- Each main node should have ONLY 2 child nodes\n"
                "- Keep all names short, 2-4 words max\n"
                "- Use REAL content from the summary, not placeholders\n"
                "- Return ONLY the JSON, no explanation, no markdown backticks\n\n"
                f"Summary:\n{summary_text}"
            )
        }]
    )

    import json
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'^```\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "name": "Mind Map",
            "type": "general",
            "children": [{"name": "Could not parse. Try regenerating."}]
        }


import re
import json

def generate_quiz(summary_text: str) -> list:
    prompt = (
        "Based on the following book summary, generate exactly 5 multiple choice questions.\n"
        "Each question must have 4 options labeled A, B, C, D.\n"
        "Return ONLY a single valid JSON array containing 5 objects. No explanation, no markdown, no backticks.\n"
        "Each object must have exactly these keys: question, options, answer.\n"
        "Example of exact format to follow:\n"
        '[{"question": "What is X?", "options": {"A": "one", "B": "two", "C": "three", "D": "four"}, "answer": "A"}, {"question": "What is Y?", "options": {"A": "one", "B": "two", "C": "three", "D": "four"}, "answer": "B"}]\n\n'
        f"Summary:\n{summary_text}"
    )

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()

    # Strip markdown code blocks if present
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("["):
                raw = part
                break

    # Fix "question1", "question2" keys -> "question"
    import re, json
    raw = re.sub(r'"question\d+"', '"question"', raw)

    # Try parsing directly first — raw may already be valid
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Fallback: find first [ to last ]
    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON array found in response")

    return json.loads(raw[start:end+1])