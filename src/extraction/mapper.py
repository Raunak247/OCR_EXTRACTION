# src/extraction/mapper.py
from src.extraction.regex_pattern import PATTERNS
from src.extraction.sanitizer import sanitize_text
import re

def map_field_using_regex(text: str):
    text = sanitize_text(text)
    for k, pat in PATTERNS.items():
        m = re.search(pat, text)
        if m:
            return k, m.group(0)
    return None, text
