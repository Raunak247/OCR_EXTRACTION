# src/mosip/vc_issuer.py
import json
from src.mosip.sign import sign_payload
from src.mosip.qr_generator import generate_qr

from src.utilis.common import now_iso
import os

def build_vc(subject: dict, verification_report: dict, doc_id: str, out_dir: str):
    vc = {
        "id": f"vc:{doc_id}",
        "type": ["VerifiableCredential", "IdentityCredential"],
        "issuanceDate": now_iso(),
        "issuer": {
            "id": "did:example:issuer",
            "name": "OCR Extraction Demo Issuer"
        },
        "credentialSubject": subject,
        "evidence": verification_report
    }
    sig = sign_payload(vc)
    vc["proof"] = {"type": "MOCK", "signature": sig}
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"{doc_id}_vc.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(vc, f, indent=2)
    # QR
    qr_path = os.path.join(out_dir, f"{doc_id}_vc_qr.png")
    generate_qr(json.dumps(vc), qr_path)
    return {"vc_path": json_path, "qr_path": qr_path, "vc": vc}
