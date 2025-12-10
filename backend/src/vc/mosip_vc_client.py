# src/vc/mosip_vc_client.py
import json
from src.utils.logger import get_logger
logger = get_logger("mosip_vc")

def sign_payload_with_mosip(payload: dict, cfg: dict = None):
    """
    Mock of MOSIP signing. If MOSIP config provided, call real API.
    For prototype we create a 'signed' wrapper.
    """
    signed = {
        "signed_payload": payload,
        "signature": "MOCK_SIGNATURE_abc123",
        "signed_at": "mock"
    }
    logger.info("Mock-signed VC payload")
    return signed
