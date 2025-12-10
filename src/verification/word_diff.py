# src/verification/word_diff.py
from difflib import SequenceMatcher
from typing import Dict

def word_similarity(a: str, b: str) -> float:
    if not a and not b:
        return 100.0
    if not a or not b:
        return 0.0
    s = SequenceMatcher(None, a, b)
    return round(s.ratio() * 100, 2)

def missing_words(a: str, b: str):
    """
    Returns words present in 'a' but not in 'b' (case-insensitive)
    """
    wa = set((a or "").upper().split())
    wb = set((b or "").upper().split())
    return list(wa - wb)
