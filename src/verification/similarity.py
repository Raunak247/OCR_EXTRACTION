# src/verification/similarity.py
from rapidfuzz import fuzz

def compute_similarity(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return fuzz.token_sort_ratio(a,b) / 100.0
