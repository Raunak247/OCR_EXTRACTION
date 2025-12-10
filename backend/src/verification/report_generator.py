# src/verification/report_generator.py
from datetime import datetime

def create_report(document_id: str, field_results: dict):
    overall = sum(v.get("similarity",0) for v in field_results.values()) / max(len(field_results),1)
    status = "VERIFIED" if overall >= 0.8 else ("REVIEW" if overall >= 0.6 else "REJECTED")
    return {
        "document_id": document_id,
        "timestamp": datetime.utcnow().isoformat()+"Z",
        "overall_score": round(overall,3),
        "status": status,
        "fields": field_results
    }
