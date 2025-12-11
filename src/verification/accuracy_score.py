# src/verification/accuracy_score.py
def compute_overall_score(per_field_results: dict) -> float:
    """
    Aggregate per-field similarity into overall percentage (0-100).
    Simple weighted average: all fields equal weight.
    """
    if not per_field_results:
        return 0.0
    scores = []
    for v in per_field_results.values():
        try:
            scores.append(float(v.get("similarity", 0.0)))
        except Exception:
            scores.append(0.0)
    overall = sum(scores) / len(scores)
    return round(overall, 2)
