# src/utils/common.py
import datetime

def timestamp():
    """Return current UTC timestamp in ISO format."""
    return datetime.datetime.utcnow().isoformat() + "Z"
