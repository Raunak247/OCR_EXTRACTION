import io
from fastapi.testclient import TestClient
from PIL import Image
from src.main import app

client = TestClient(app)

def create_dummy_image():
    img = Image.new("RGB", (400, 200), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def test_extract_api():
    buf = create_dummy_image()

    response = client.post(
        "/api/extract",
        files={"file": ("test.png", buf, "image/png")}
    )

    assert response.status_code == 200
    result = response.json()

    assert "status" in result
    assert result["status"] in ["success", "error"]

    print("Extract API Response:", result)
