from datetime import datetime
from PyPDF2 import PdfFileMerger, PdfFileReader
import logging
from pathlib import Path


AGORA = datetime.now().strftime("%H-%M-%S")
LOG_FILE = f"e:\Desktop\ERRO_junta-pdf-{AGORA}.log"
logger = logging.getLogger(__name__)
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(LOG_FILE, mode="a")
handler.setLevel(logging.DEBUG)
handler.setFormatter(log_format)
logger.addHandler(handler)


def merge_pdfs(path_list: list([Path]), destination: Path) -> None:
    """
    Receives a list contaning PDF files paths and tries to merge them in a
    single PDF and saves it to the user Desktop.
    """

    pdf_merger = PdfFileMerger()
    
    with open(destination, 'wb') as pdf:
        for path in path_list:
            try:
                with open(path, "rb") as file:
                    new_pdf = PdfFileReader(file)
                    pdf_merger.append(new_pdf)
            except:
                logger.error(path, exc_info=True)
        pdf_merger.write(pdf)
