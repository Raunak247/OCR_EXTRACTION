# src/utilis/common.py

import time
import os

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

def now_iso() -> str:
    """Return current timestamp in ISO-8601 format"""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

