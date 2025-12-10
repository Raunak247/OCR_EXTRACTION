# src/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import extract_api, verify_api, vc_api, health

app = FastAPI(title="OCR Extraction & Verification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(extract_api.router, prefix="/api")
app.include_router(verify_api.router, prefix="/api")
app.include_router(vc_api.router, prefix="/api")
app.include_router(health.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
