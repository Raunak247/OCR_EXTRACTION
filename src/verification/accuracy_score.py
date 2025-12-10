# src/verification/accuracy_score.py
from rapidfuzz import fuzz

def fuzzy_score(a: str, b: str) -> float:
    if not a and not b:
        return 100.0
    if not a or not b:
        return 0.0
    return round(fuzz.token_set_ratio(a, b), 2)
