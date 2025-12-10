# src/verification/compare_fields.py
from src.verification.normalizer import normalize_value
from src.verification.similarity import compute_similarity

def compare(extracted: str, submitted: str):
    ne = normalize_value(extracted)
    ns = normalize_value(submitted)
    sim = compute_similarity(ne, ns)
    match = sim >= 0.75
    return {"similarity": round(sim,3), "match": match}
