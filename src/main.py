from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.extract_api import router as extract_router
from src.routes.verify_api import router as verify_router
from src.routes.health_api import router as health_router


app = FastAPI(
    title="OCR Extraction & Verification API",
    version="1.0.0",
    description="Backend for OCR extraction, verification & quality scoring"
)


# ---------------------- CORS (allow frontend later) ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------- Register Routes ----------------------
app.include_router(extract_router)   # /api/extract
app.include_router(verify_router)    # /api/verify
app.include_router(health_router)    # /api/health


# ---------------------- Root ----------------------
@app.get("/")
def root():
    return {
        "message": "OCR Extraction API Running Successfully",
        "endpoints": {
            "extract": "/api/extract",
            "verify": "/api/verify",
            "health": "/api/health"
        }
    }
