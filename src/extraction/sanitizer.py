# src/extraction/sanitizer.py
import re

def normalize_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()

def uppercase_and_strip(s: str) -> str:
    return normalize_whitespace(s).upper()
