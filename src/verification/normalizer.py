# src/verification/normalizer.py
import re

def normalize_value(text: str) -> str:
    if text is None:
        return ""
    s = str(text).strip()
    s = s.replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s)
    s = s.upper().strip()
    return s
