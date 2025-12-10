from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.services.verify_service import VerifyService

router = APIRouter()

class VerifyRequest(BaseModel):
    document_id: str
    user_values: Dict[str, Any]

svc = VerifyService()

@router.post("/verify")
def verify(req: VerifyRequest):
    """
    Verify against previously extracted OCR result.
    Body: { "document_id": "...", "user_values": { "name": "Raunak", ... } }
    """
    try:
        report = svc.verify(req.document_id, req.user_values)
        return {"status": "success", "report": report}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
