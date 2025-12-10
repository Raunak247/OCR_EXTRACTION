# src/verification/normalizer.py
import re
def normalize_value(text: str) -> str:
    if text is None:
        return ""
    s = str(text).upper().strip()
    s = s.replace("\n"," ").replace("\r"," ")
    s = re.sub(r"[^A-Z0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s
