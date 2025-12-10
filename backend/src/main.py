from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.routes.extract_api import router as extract_router
from src.routes.verify_api import router as verify_router
from src.routes.health_api import router as health_router

import logging

# ----------------------------------------------------
# App Initialization
# ----------------------------------------------------
app = FastAPI(
    title="OCR Extraction & Verification API",
    description="Handles OCR extraction, verification and health monitoring.",
    version="1.0.0"
)

# ----------------------------------------------------
# Logging
# ----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ----------------------------------------------------
# CORS
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # for production replace "*" with client domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Global Exception Handler
# ----------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"ERROR: {exc}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc)}
    )

# ----------------------------------------------------
# Routers
# ----------------------------------------------------
app.include_router(extract_router, prefix="/api", tags=["OCR Extraction"])
app.include_router(verify_router, prefix="/api", tags=["Verification"])
app.include_router(health_router, prefix="/api", tags=["Health Check"])

# ----------------------------------------------------
# Root Endpoint
# ----------------------------------------------------
@app.get("/")
def root():
    return {"message": "OCR API Running Successfully!"}

