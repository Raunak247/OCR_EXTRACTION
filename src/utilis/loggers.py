# src/utilis/loggers.py
import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str = "ocr_extraction", log_path: str = None, level=logging.INFO):
    loggers = logging.getLogger(name)
    if loggers.handlers:
        return loggers

    loggers.setLevel(level)

    if log_path is None:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        logs_dir = os.path.join(base, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        log_path = os.path.join(logs_dir, f"{name}.log")

    fh = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
    fh.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    loggers.addHandler(fh)
    loggers.addHandler(ch)
    loggers.propagate = False
    return loggers
