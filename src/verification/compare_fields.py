from rapidfuzz import fuzz
from src.verification.normalizer import normalize_value

def compare(extracted, submitted):
    """
    Accept extracted (string or dict) and submitted (string).
    Returns:
      {
        "extracted": str,
        "submitted": str,
        "similarity": float (0-100),
        "match": bool,
        "reason": "..."
      }
    """
    if isinstance(extracted, dict):
        # if extracted contains nested structure, try 'text' key
        extracted_text = extracted.get("text") or extracted.get("value") or ""
    else:
        extracted_text = extracted or ""

    a = normalize_value(extracted_text)
    b = normalize_value(str(submitted))

    if not a and not b:
        similarity = 100.0
    elif not a or not b:
        similarity = 0.0
    else:
        similarity = fuzz.token_sort_ratio(a, b)

    match = similarity >= 75.0
    reason = "match" if match else "similarity_below_threshold"
    return {
        "extracted": extracted_text,
        "submitted": submitted,
        "similarity": round(similarity, 2),
        "match": match,
        "reason": reason
    }
