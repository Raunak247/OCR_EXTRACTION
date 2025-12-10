# src/utils/path_utils.py
from pathlib import Path

def ensure_dir(path):
    """Create folder if not exists."""
    Path(path).mkdir(parents=True, exist_ok=True)

def path_exists(path):
    """Check if path exists."""
    return Path(path).exists()

def join(*parts):
    """Join path parts safely."""
    return str(Path(*parts))
