# src/verification/final_verifier.py
from typing import Dict
from src.verification.compare_engine import compare_field

def final_verification(ocr_extracted: Dict, user_values: Dict):
    """
    ocr_extracted: dict of fields (name,dob,address,id_number,document_type)
    user_values: dict with same keys
    returns summary with per-field scores and overall score
    """
    fields = ["name", "dob", "address", "id_number"]
    results = {}
    total = 0.0
    count = 0
    for f in fields:
        o = ocr_extracted.get(f)
        u = user_values.get(f)
        res = compare_field(o, u)
        results[f] = res
        total += res["score"]
        count += 1
    overall = round(total / count, 2) if count else 0.0
    status = "verified" if overall >= 85 else ("partial" if overall >= 50 else "unverified")
    return {"overall_score": overall, "status": status, "fields": results}
