from pathlib import Path

def create_doc_folders(doc_id: str) -> str:
    base = Path("files") / doc_id
    for sub in ("raw", "processed", "crops", "ocr", "verification", "report"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    return str(base)

def save_raw_file(doc_id: str, upload_file):
    """
    Save UploadFile to files/<doc_id>/raw/<filename>
    If upload_file is bytes (already read), handle it too.
    Returns full path as string.
    """
    base = Path("files") / doc_id / "raw"
    base.mkdir(parents=True, exist_ok=True)
    if hasattr(upload_file, "filename"):
        filename = upload_file.filename
        path = base / filename
        # UploadFile is async, route passes UploadFile, so read bytes in route or here
        try:
            data = upload_file.file.read()
        except Exception:
            # fallback: maybe upload_file is bytes
            data = b""
        with open(path, "wb") as f:
            f.write(data)
        return str(path)
    else:
        # upload_file is bytes
        filename = f"{doc_id}.bin"
        path = base / filename
        with open(path, "wb") as f:
            f.write(upload_file)
        return str(path)

def ensure_doc_folder(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path
