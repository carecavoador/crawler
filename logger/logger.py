import logging
import os
from pathlib import Path

LOG_FILE = Path(os.path.expanduser("~/Desktop"), "Entrada", "crawler.log")
logger = logging.getLogger(__name__)
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(LOG_FILE, mode="a")
handler.setLevel(logging.DEBUG)
handler.setFormatter(log_format)
logger.addHandler(handler)