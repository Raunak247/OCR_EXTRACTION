# src/routes/vc_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.verify_service import VerifyService
from src.vc.vc_payload_builder import build_vc_payload
from src.vc.mosip_vc_client import sign_payload_with_mosip
from src.vc.qr_generator import generate_qr_for_payload
from pathlib import Path
from src.utils.file_manager import ensure_doc_folder, save_json

router = APIRouter()

class VCRequest(BaseModel):
    document_id: str
    issuer_name: str = "Demo Issuer"

@router.post("/vc/issue")
def issue_vc(req: VCRequest):
    vs = VerifyService()
    # load verification result
    base = Path("files") / req.document_id
    ver_path = base / "verification" / "verification.json"
    if not ver_path.exists():
        raise HTTPException(status_code=404, detail="verification result not found")
    report = ver_path.read_text(encoding="utf8")
    import json
    verification_report = json.loads(report)
    payload = build_vc_payload(req.document_id, verification_report, issuer={"name": req.issuer_name, "id":"did:demo:issuer"})
    signed = sign_payload_with_mosip(payload)
    qr_path = base / "report" / "vc_qr.png"
    generate_qr_for_payload(signed, qr_path)
    save_json(base / "report" / "vc_signed.json", signed)
    return {"status":"ok", "vc": signed, "qr": str(qr_path)}
