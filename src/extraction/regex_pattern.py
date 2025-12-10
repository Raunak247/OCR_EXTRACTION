# src/extraction/regex_patterns.py
import re

# Some basic patterns (expand as needed)
PATTERNS = {
    "dob": r"(\d{2}[-\/]\d{2}[-\/]\d{4})|(\d{4}[-\/]\d{2}[-\/]\d{2})",
    "id_number": r"[A-Z0-9\-]{6,}",
    "pincode": r"\b\d{6}\b",
    "year": r"\b(19|20)\d{2}\b",
}
