# src/vc/vc_payload_builder.py
import json
from datetime import datetime

def build_vc_payload(document_id: str, verification_report: dict, issuer: dict = None):
    payload = {
        "id": f"vc:{document_id}",
        "issuanceDate": datetime.utcnow().isoformat()+"Z",
        "issuer": issuer or {"name":"Demo Issuer","id":"did:demo:issuer"},
        "credentialSubject": {
            "document_id": document_id,
            "verification": verification_report
        }
    }
    return payload
