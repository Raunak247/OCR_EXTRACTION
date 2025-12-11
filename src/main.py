from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.vc_api import router as vc_router
from frontend.src.app.include_router(vc_router, prefix="/api/vc")

from src.routes.health_api import router as health_router
from src.routes.extract_api import router as extract_router
from src.routes.verify_api import router as verify_router
from src.routes.vc_api import router as vc_router

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


app = FastAPI(title="OCR Extraction & Verification")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(extract_router, prefix="/api")
app.include_router(verify_router, prefix="/api")
app.include_router(vc_router, prefix="/api")
from src.utilis.common import ensure_dir

for folder in ["uploads", "processed", "extracted", "output", "storage"]:
    ensure_dir(folder)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router, prefix="/api")
app.include_router(extract_router, prefix="/api")