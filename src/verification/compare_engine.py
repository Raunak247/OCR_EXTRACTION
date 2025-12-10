# src/verification/compare_engine.py
from src.verification.word_diff import word_similarity, missing_words
from src.verification.accuracy_score import fuzzy_score

def compare_field(ocr_value: str, user_value: str):
    sim = fuzzy_score(ocr_value or "", user_value or "")
    missing = missing_words(ocr_value or "", user_value or "")
    return {"ocr": ocr_value, "user": user_value, "score": sim, "missing_words": missing}
