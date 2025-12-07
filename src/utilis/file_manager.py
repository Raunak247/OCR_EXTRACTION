# src/utils/file_manager.py
from pathlib import Path
import aiofiles

def create_doc_folders(doc_id: str) -> str:
    base = Path("files") / doc_id
    for sub in ("raw", "processed", "crops", "ocr", "report"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    return str(base)

async def save_raw_file(doc_id: str, upload_file) -> str:
    base = Path("files") / doc_id
    raw_dir = base / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    filename = upload_file.filename
    path = raw_dir / filename
    data = await upload_file.read()
    async with aiofiles.open(path, "wb") as f:
        await f.write(data)
    return str(path)
