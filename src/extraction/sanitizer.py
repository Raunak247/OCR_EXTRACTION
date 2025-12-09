# src/extraction/sanitizer.py
import re

class Sanitizer:
    """
    Clean and normalize the raw OCR text before extraction.
    """
    def clean(self, text: str) -> str:
        if not text:
            return ""
        # Remove weird control chars, normalize whitespace
        t = re.sub(r"[\r\t]+", " ", text)
        t = re.sub(r"\s+", " ", t)
        return t.strip()
