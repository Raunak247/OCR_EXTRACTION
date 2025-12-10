# src/config.py
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))

UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(BASE_DIR, "..", "uploads"))
FILES_DIR = os.getenv("FILES_DIR", os.path.join(BASE_DIR, "..", "files"))
PROCESSED_DIR = os.getenv("PROCESSED_DIR", os.path.join(BASE_DIR, "..", "processed"))

# TrOCR config
TROCR_MODEL = os.getenv("TROCR_MODEL", "microsoft/trocr-base-printed")
MOSIP_BASE_URL = os.getenv("MOSIP_BASE_URL", "")
MOSIP_API_KEY = os.getenv("MOSIP_API_KEY", "")
