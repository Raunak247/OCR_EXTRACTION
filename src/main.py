from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.extract_api import router as extract_router
from src.routes.verify_api import router as verify_router
from src.routes.health_api import router as health_router

app = FastAPI(title="OCR Extraction & Verification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(extract_router, prefix="/api")
app.include_router(verify_router, prefix="/api")
app.include_router(health_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "OCR API Running!"}
