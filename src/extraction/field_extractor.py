# src/extraction/field_extractor.py
import re
from typing import Dict, Optional

from src.extraction.sanitizer import uppercase_and_strip

# Aadhaar spelling fix
try:
    from src.extraction import aadhaar_rules
except:
    from src.extraction import adhaar_rules as aadhaar_rules

from src.extraction import pan_rules, voterid_rules


class FieldExtractor:
    """
    Final version: usable by ExtractService
    """

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        result = {
            "name": None,
            "dob": None,
            "address": None,
            "id_number": None,
            "document_type": "unknown"
        }

        if not text:
            return result

        txt = uppercase_and_strip(text)

        # ---------------- Aadhaar ----------------
        aadhar = None
        try:
            aadhar = aadhaar_rules.find_aadhaar(txt)
        except:
            pass

        if aadhar:
            result["document_type"] = "aadhaar"
            result["id_number"] = aadhar

        # ---------------- PAN ----------------
        pan = None
        try:
            pan = pan_rules.find_pan(txt)
        except:
            pass

        if pan:
            result["document_type"] = "pan"
            result["id_number"] = pan

        # ---------------- Voter ID ----------------
        voter = None
        try:
            voter = voterid_rules.find_voterid(txt)
        except:
            pass

        if voter:
            result["document_type"] = "voterid"
            result["id_number"] = voter

        # ---------------- Name ----------------
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        for ln in lines[:10]:
            if 2 <= len(ln.split()) <= 6:
                result["name"] = ln
                break

        # ---------------- DOB ----------------
        dob = re.search(r"\d{2}[-/]\d{2}[-/]\d{4}", txt)
        if dob:
            result["dob"] = dob.group(0)

        # ---------------- Address ----------------
        for ln in reversed(lines):
            if len(ln) > 40:
                result["address"] = ln
                break

        return result


# backward compatibility
def extract_fields_from_text(text: str):
    return FieldExtractor().extract(text)
