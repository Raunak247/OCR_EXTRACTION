# src/utils/common.py
import uuid
import datetime

def new_doc_id(prefix="DOC"):
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"
