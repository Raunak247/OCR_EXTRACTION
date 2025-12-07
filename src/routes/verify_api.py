# src/routes/verify_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.services.verify_service import VerifyService

router = APIRouter()

class VerifyRequest(BaseModel):
    document_id: str
    user_values: Dict[str, Any]

@router.post("/verify")
def verify(req: VerifyRequest):
    svc = VerifyService()
    try:
        report = svc.verify(req.document_id, req.user_values)
        return report
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
