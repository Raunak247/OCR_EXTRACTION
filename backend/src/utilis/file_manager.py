# src/utils/file_manager.py
from pathlib import Path
import shutil
import uuid
import os

BASE_FILES = Path("files")

def ensure_doc_folder(doc_id: str = None) -> Path:
    """
    Create and return document folder path files/<doc_id> with subdirs.
    If doc_id not provided, create a new random one.
    """
    if doc_id is None:
        doc_id = uuid.uuid4().hex[:8]
    base = BASE_FILES / doc_id
    for sub in ("raw", "processed", "crops", "ocr", "verification", "report"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    return base

def save_upload_bytes(doc_id: str, filename: str, data: bytes) -> Path:
    base = ensure_doc_folder(doc_id)
    p = base / "raw" / filename
    with open(p, "wb") as f:
        f.write(data)
    return p

def move_to_processed(src: Path, doc_id: str, name: str) -> Path:
    base = ensure_doc_folder(doc_id)
    dst = base / "processed" / name
    shutil.copy2(src, dst)
    return dst

def save_json(p: Path, data: dict):
    import json
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf8")
