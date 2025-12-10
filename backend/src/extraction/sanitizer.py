# src/extraction/sanitizer.py
import re
def sanitize_text(s: str):
    if s is None:
        return ""
    s = s.replace("\n"," ").replace("\r"," ").strip()
    s = re.sub(r"\s+", " ", s)
    return s
