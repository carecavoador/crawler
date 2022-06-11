from sys import argv
import os
from datetime import datetime
from PyPDF2 import PdfFileMerger, PdfFileReader
import logging
from pathlib import Path


NOW = datetime.now().strftime("%H-%M-%S")
DESKTOP = os.path.join(os.environ["HOMEPATH"], "Desktop")
MERGED_PDF = os.path.join(DESKTOP, f"junta-pdf-{NOW}.pdf")
LOG_FILE = f"e:\Desktop\ERRO_junta-pdf-{NOW}.log"

logger = logging.getLogger(__name__)
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(LOG_FILE, mode="a")
handler.setLevel(logging.DEBUG)
handler.setFormatter(log_format)
logger.addHandler(handler)


def merge_pdfs(path_list: list[Path]) -> None:
    """
    Receives a list contaning PDF files paths and tries to merge them in a
    single PDF and saves it to the user Desktop.
    """

    pdf_merger = PdfFileMerger()
    
    with open(MERGED_PDF, 'wb') as pdf:
        for path in path_list:
            try:
                with open(path, "rb") as file:
                    new_pdf = PdfFileReader(file)
                    pdf_merger.append(new_pdf)
            except:
                logger.error(path, exc_info=True)
        pdf_merger.write(pdf)


if __name__ == '__main__':
    PROOF_FILES = [
        r"C:\Users\Everton Souza\OneDrive\dev\projetos\python\crawler\Arquivos\Print Digital\09-06-2022\36652_V14_103077_Juliatto - Linguica Tipo Calabresa 8g - Multivac.pdf",
        r"C:\Users\Everton Souza\OneDrive\dev\projetos\python\crawler\Arquivos\Print Digital\09-06-2022\620415_V2 - Digital.pdf.zip",
        r"C:\Users\Everton Souza\OneDrive\dev\projetos\python\crawler\Arquivos\Print Digital\09-06-2022\717716_V1 GMG.pdf",
        r"C:\Users\Everton Souza\OneDrive\dev\projetos\python\crawler\Arquivos\Print Digital\09-06-2022\717788_V1 Digital.pdf"
    ]
    PROOF_FILES = [Path(p) for p in PROOF_FILES]
    print(PROOF_FILES)
    # merge_pdfs(PROOF_FILES)
