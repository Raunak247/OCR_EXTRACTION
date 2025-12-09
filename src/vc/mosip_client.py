# src/vc/mosip_vc_client.py
import os
import requests

MOSIP_BASE_URL = os.environ.get("MOSIP_BASE_URL", "")  # set in .env if available
MOSIP_API_KEY = os.environ.get("MOSIP_API_KEY", "")

class MOSIPVCClient:
    """
    Minimal connector for MOSIP VC issuance.
    If MOSIP is not reachable, returns a mock signed payload for demo.
    """
    def __init__(self, base_url=MOSIP_BASE_URL):
        self.base = base_url.rstrip("/")

    def issue_vc(self, unsigned_payload: dict) -> dict:
        if not self.base:
            # mock response for offline demo
            return {"status": "mock", "message": "MOSIP not configured", "vc": unsigned_payload}
        url = f"{self.base}/vc/issue"
        headers = {"Authorization": f"Bearer {MOSIP_API_KEY}", "Content-Type": "application/json"}
        r = requests.post(url, json=unsigned_payload, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()
