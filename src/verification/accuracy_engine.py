# src/verification/accuracy_engine.py
from statistics import mean

def compute_overall_score(field_scores: dict) -> float:
    """
    field_scores: { "name": {"match_score": 85}, "address": {"match_score": 72} }
    returns overall percentage 0-100
    """
    if not field_scores:
        return 0.0
    scores = [v.get("match_score", 0) for v in field_scores.values()]
    return round(mean(scores), 2)
