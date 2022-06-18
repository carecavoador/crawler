import os
import json
import logging
from pathlib import Path


CONFIG = json.load(open("C:\Projetos\Python\crawler\config.json", "r", encoding="utf-8"))

LOG_FILE = Path(CONFIG["jobs_folder"], "crawler.log")
logger = logging.getLogger(__name__)
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

handler = logging.FileHandler(LOG_FILE, mode="a")
handler.setLevel(logging.DEBUG)
handler.setFormatter(log_format)
logger.addHandler(handler)