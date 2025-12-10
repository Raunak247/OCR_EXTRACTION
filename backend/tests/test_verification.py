from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_verification_api():
    payload = {
        "text": "Invoice Number 12345",
        "rule": "contains_number"
    }

    response = client.post("/api/verify", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] in ["verified", "failed", "error"]

    print("Verification API Response:", data)
