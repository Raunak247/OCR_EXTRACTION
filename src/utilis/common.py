# src/utilis/common.py

import time
import os
from datetime import datetime

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def ts() -> str:
    """Returns timestamp string"""
    return str(int(time.time()))

def ensure_dir(path: str):
    """Safe directory creation"""
    if not os.path.exists(path):
        os.makedirs(path)

def safe_filename(name: str) -> str:
    """Removes bad characters from filenames"""
    return "".join(c for c in name if c.isalnum() or c in "._-").rstrip()


