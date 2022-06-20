import re
from pathlib import Path
from PyPDF2 import PdfFileReader
from osnumber import OSNumber


class Job:
    def __init__(self, os_number: OSNumber, pdf_file: Path) -> None:
        self.os = os_number
        self.pdf = pdf_file
        self.needs_layout: bool = False
        self.needs_proof: bool = False
        self.profile: str = ""
        self.read_job_data_from_pdf(self.pdf)

    def __repr__(self) -> str:
        return f"OS_{self.os.number}_V{self.os.version}"
    
    def read_job_data_from_pdf(self, _pdf: Path) -> None:
        """
        Reads a PDF file and extract it's text to look for the job
        information.
        """
        profile = ""
        layout = False
        proof = False
        
        with open(_pdf, "rb") as f:
            reader = PdfFileReader(f)
            page_one = reader.pages[0]
            text = page_one.extract_text().split("\n")
        
        for line in text:
            if line == text[14]:
                self.profile = "_Perfil_"
                self.profile += re.search("(.+)Fechamento:", line).groups(1)[0]
            elif line.startswith("Print Layout"):
                self.needs_layout = True
            elif line.startswith("Prova Digital"):
                self.needs_proof = True
