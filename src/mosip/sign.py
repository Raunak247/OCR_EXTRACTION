# src/mosip/sign.py
"""
Mock signing module. Replace with MOSIP signing calls as required.
"""
import json
from src.utils.logger import logger

def sign_payload(payload: dict, private_key_path: str = None):
    # MOCK: produce a fake signature string
    # Replace: call MOSIP signing endpoint or cryptographic library using a real key
    signature = "MOCK_SIGN_" + payload.get("id", "noid")
    logger.info("Mock-signed payload id=%s", payload.get("id"))
    return signature
