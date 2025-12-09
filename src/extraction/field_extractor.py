# src/extraction/field_extractor.py
from src.extraction.regex_pattern import find_name, find_dob, find_id
from sanitizer import Sanitizer

class FieldExtractor:
    """
    Lightweight field extractor using regex rules and simple heuristics.
    Returns a dict with common fields and raw_text.
    """
    def __init__(self):
        self.s = Sanitizer()

    def extract_fields(self, raw_text: str):
        txt = self.s.clean(raw_text)
        name = find_name(txt)
        dob = find_dob(txt)
        id_no = find_id(txt)

        # address naive: everything after "Address" or "ADDR" (improve later)
        address = None
        for marker in ("address:", "addr:", "ADDRESS:", "Address:"):
            if marker in raw_text:
                address = raw_text.split(marker, 1)[1].split("\n")[0].strip()
                break

        return {
            "name": name,
            "dob": dob,
            "address": address,
            "id_number": id_no,
            "raw_text": txt
        }
