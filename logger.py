"""
MiroOrca Logger
Provides rotating file + console logging with UTF-8 support.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

LOGS_DIR = os.path.join(os.path.dirname(__file__), "../../logs")


def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Create and return a named logger with:
    - Console handler: INFO level, clean format
    - File handler: DEBUG level, detailed format, rotating 5MB x 3 files
    """
    os.makedirs(LOGS_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.DEBUG)

    # ── Console handler ────────────────────────────────────────────
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(log_level)
    console.setFormatter(logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S"
    ))
    # Ensure UTF-8 output on Windows
    if hasattr(console.stream, "reconfigure"):
        try:
            console.stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    logger.addHandler(console)

    # ── File handler ───────────────────────────────────────────────
    log_file = os.path.join(LOGS_DIR, "miroorca.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s:%(lineno)d  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(file_handler)

    return logger
