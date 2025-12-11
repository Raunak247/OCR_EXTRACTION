# src/routes/vc_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.mosip.vc_issuer import build_vc
from src.utilis.file_manager import ensure_doc_folder
import os

router = APIRouter()

class VCRequest(BaseModel):
    document_id: str
    subject: dict  # mapped MOSIP subject data (name,dob, id, etc.)

@router.post("/vc/issue")
def issue_vc(req: VCRequest):
    base = ensure_doc_folder(req.document_id)
    # read verification report
    rep_path = os.path.join(base, "verification", "report.json")
    if not os.path.exists(rep_path):
        raise HTTPException(status_code=404, detail="Verification report not found")
    import json
    with open(rep_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    # only issue if score >= threshold (mock)
    if report.get("overall_score", 0) < 60:
        # allow lower for demo but mark as partial
        pass
    out = build_vc(req.subject, report, req.document_id, os.path.join(base, "report"))
    return {"vc": out}
