from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader
from logger import logger as log

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
                log.logger.error(path, exc_info=True)
        pdf_merger.write(pdf)
