# src/extraction/pan_rules.py
import re
PAN_RE = re.compile(r"\b([A-Z]{5}\d{4}[A-Z])\b")

def find_pan(text: str):
    m = PAN_RE.search(text)
    if m:
        return m.group(1)
    return None
