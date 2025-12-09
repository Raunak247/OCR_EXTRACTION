# src/extraction/regex_patterns.py
import re

# Simple regex heuristics — tweak for specific doc formats
NAME_PATTERNS = [
    r"(?:Name|NAME|name)[:\-\s]+([A-Z][A-Za-z\s]{2,80})",
    r"([A-Z][a-z]+\s[A-Z][a-z]+)"  # fallback: two capitalized words
]

DOB_PATTERNS = [
    r"(?:DOB|D\.O\.B|Date of Birth|Birth Date)[:\-\s]+(\d{2}[\/\-\s]\d{2}[\/\-\s]\d{4})",
    r"(\d{2}[\/\-\s]\d{2}[\/\-\s]\d{4})"
]

ID_PATTERNS = [
    r"\b([A-Z0-9]{4,20})\b",  # generic fallback; validate later
]


def _search_first(patterns, text):
    for p in patterns:
        m = re.search(p, text)
        if m:
            # take last group if exists else the whole match
            if m.groups():
                return m.group(m.lastindex or 1).strip()
            return m.group(0).strip()
    return None


def find_name(text: str):
    return _search_first(NAME_PATTERNS, text)


def find_dob(text: str):
    return _search_first(DOB_PATTERNS, text)


def find_id(text: str):
    # more specific validation can be applied per doc type
    candidate = _search_first(ID_PATTERNS, text)
    if candidate and len(candidate) >= 6:
        return candidate
    return None
