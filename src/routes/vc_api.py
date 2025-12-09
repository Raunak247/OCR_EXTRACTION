# src/routes/vc_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.vc_service import VCService
from src.utilis.validators import is_valid_docid

router = APIRouter()
vc_service = VCService()

class VCRequest(BaseModel):
    document_id: str
    mapped_subject: dict
    verification: dict

@router.post("/vc/issue")
def issue_vc(req: VCRequest):
    if not is_valid_docid(req.document_id):
        raise HTTPException(status_code=400, detail="Invalid document_id")
    resp = vc_service.create_and_issue_vc(req.document_id, req.mapped_subject, req.verification)
    return resp
