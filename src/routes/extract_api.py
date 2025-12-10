from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from src.services.extract_service import ExtractService

router = APIRouter()

svc = ExtractService()

@router.post("/extract")
async def extract_document(file: UploadFile = File(...), template_hint: Optional[str] = None):
    """
    Upload file (pdf/png/jpg). Returns extraction JSON (document_id, fields, quality).
    """
    if file.content_type not in ("application/pdf", "image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    result = await svc.process_document(file, template_hint=template_hint)
    return result
