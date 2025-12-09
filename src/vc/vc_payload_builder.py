# src/vc/vc_payload_builder.py
import uuid
import datetime
from src.utilis.common import ts

class VCPayloadBuilder:
    """
    Build a basic Verifiable Credential payload (unsigned).
    MOSIP will sign & issue the final VC; keep payload compatible with MOSIP schema.
    """
    def build_payload(self, doc_id: str, mapped_subject: dict, verification: dict) -> dict:
        payload = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "id": f"urn:uuid:{uuid.uuid4()}",
            "type": ["VerifiableCredential", "MOSIPCredential"],
            "issuer": "urn:org:your-org:ocr-service",
            "issuanceDate": ts(),
            "credentialSubject": {
                "docId": doc_id,
                "subject": mapped_subject,
                "verification": verification
            }
        }
        return payload
