"""
Custom logger module for the project.
Handles log formatting, file logging, and console output.
"""

import logging
import os
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configure root logger once
logger_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s():%(lineno)d- %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File handler
file_handler = logging.FileHandler(LOG_DIR / "application.log")
file_handler.setFormatter(logger_format)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logger_format)
console_handler.setLevel(logging.DEBUG)

# Root handler
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

logger = logging.getLogger("yt-stream-downloader")
logger.setLevel(logging.INFO)
