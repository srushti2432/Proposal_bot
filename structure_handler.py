import re
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

from qdrant_handler import semantic_search

# Load .env + configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def parse_structure(structure_input: str) -> list:
    """
    Accepts ANY format: JSON, YAML (if PyYAML is used), bullet/numbered list,
    key: value pairs, comma-separated, or plain text lines.
    Returns a clean list of sections.
    """
    s = structure_input.strip()
    if not s:
        return []

    # Try JSON
    try:
        parsed = json.loads(s)
        if isinstance(parsed, dict):
            return list(parsed.keys())
        elif isinstance(parsed, list):
            return [str(x) for x in parsed]
    except:
        pass

    # Try key: value pairs
    key_value = []
    for line in s.splitlines():
        if ":" in line:
            key, _ = line.split(":", 1)
            key_value.append(key.strip())
    if key_value:
        return key_value

    # Try bullet/numbered lines
    bullets = []
    for line in s.splitlines():
        line = re.sub(r"^[\-\*\•\d\.\)]+", "", line).strip()
        if line:
            bullets.append(line)
    if bullets:
        return bullets

    # Try comma-separated
    if "," in s:
        return [x.strip() for x in s.split(",") if x.strip()]

    # Fallback: each non-empty line
    return [line.strip() for line in s.splitlines() if line.strip()]


def auto_detect_sections_and_fields(structure_input: str, document_text: str):
    """
    Combines user structure + doc context, asks Gemini for fields per section.
    Extracts JSON robustly even if Gemini adds extra text.
    """
    model = genai.GenerativeModel('gemini-1.5-pro')

    user_sections = parse_structure(structure_input)

    auto_sections = []
    top_chunks = semantic_search("main proposal sections", top_k=5)
    for chunk in top_chunks:
        lines = chunk.split("\n")
        for line in lines:
            clean = re.sub(r"[^A-Za-z0-9 ]+", "", line).strip()
            if clean and clean not in auto_sections:
                auto_sections.append(clean)

    all_sections = list(dict.fromkeys(user_sections + auto_sections))

    # ✅ Strict prompt with triple backticks — properly closed!
    prompt = f"""
You are a smart proposal assistant.
STRICT RULE: Reply with ONLY a valid JSON object inside triple backticks.
NO extra explanations.

Sections:
{all_sections}

Document context:
{document_text[:2000]}

Reply exactly as:
```json
{{
  "Section A": ["field1", "field2"],
  "Section B": ["field3"]
}}
"""
