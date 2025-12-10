# src/extraction/field_extractor.py
import re
from typing import Dict
from src.extraction.sanitizer import uppercase_and_strip
from src.extraction import aadhaar_rules, pan_rules, voterid_rules

def extract_fields_from_text(text: str) -> Dict:
    """
    Basic pipeline: detect patterns and return candidate values
    """
    result = {
        "name": None,
        "dob": None,
        "address": None,
        "id_number": None,
        "document_type": "unknown"
    }
    txt = uppercase_and_strip(text)

    # Aadhaar detection
    aad = aadhaar_rules.find_aadhaar(txt)
    if aad:
        result["id_number"] = aad
        result["document_type"] = "aadhaar"

    # PAN detection
    pan = pan_rules.find_pan(txt)
    if pan:
        result["id_number"] = pan
        result["document_type"] = "pan"

    # VoterID detection
    vid = voterid_rules.find_voterid(txt)
    if vid:
        result["id_number"] = vid
        result["document_type"] = "voterid"

    # name heuristic: lines with uppercase words and length
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    if lines:
        # pick first long-ish line as name heuristic
        for ln in lines[:6]:
            if 3 <= len(ln.split()) <= 6 and any(c.isalpha() for c in ln):
                result["name"] = ln
                break

    # DOB regex
    m = re.search(r"(\d{2}[-/]\d{2}[-/]\d{4})", txt)
    if m:
        result["dob"] = m.group(1)

    # address fallback: long line
    for ln in reversed(lines):
        if len(ln) > 30:
            result["address"] = ln
            break

    return result
