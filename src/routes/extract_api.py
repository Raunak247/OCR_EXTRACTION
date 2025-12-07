# src/routes/extract_api.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from src.services.extract_service import ExtractService

router = APIRouter()

@router.post("/extract")
async def extract_document(file: UploadFile = File(...), template_hint: Optional[str] = None):
    if file.content_type not in ("application/pdf", "image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    svc = ExtractService()
    result = await svc.process_document(file, template_hint)
    return result
