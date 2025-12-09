# src/utils/file_manager.py
# src/utils/file_manager.py
import os
from pathlib import Path
from fastapi import UploadFile

# Create doc folders and helpers
def ensure_doc_folder(path: str):
    os.makedirs(path, exist_ok=True)
    return path

def create_doc_folders(doc_id: str, base_dir: str = "files") -> str:
    base = Path(base_dir) / doc_id
    for sub in ("raw", "processed", "crops", "ocr", "verification", "report"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    return str(base)

async def save_upload_to_raw(doc_id: str, upload_file: UploadFile, base_dir: str = "files") -> str:
    """
    Save UploadFile to files/<doc_id>/raw/ and return the absolute path.
    Use this in async FastAPI endpoint: await save_upload_to_raw(...)
    """
    raw_dir = Path(base_dir) / doc_id / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    filename = Path(upload_file.filename).name
    dest = raw_dir / filename
    # read content async and write bytes
    content = await upload_file.read()
    with open(dest, "wb") as f:
        f.write(content)
    return str(dest)

def write_json(path: str, obj):
    import json
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    return path
