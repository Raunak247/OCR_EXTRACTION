# src/extraction/aadhaar_rules.py
import re

AADHAAR_RE = re.compile(r"\b(\d{4}\s?\d{4}\s?\d{4})\b")

def find_aadhaar(text: str):
    m = AADHAAR_RE.search(text)
    if m:
        return m.group(1).replace(" ", "")
    return None
