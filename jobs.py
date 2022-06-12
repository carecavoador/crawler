import os
from shutil import copy
from pathlib import Path
from PyPDF2 import PdfFileReader

from osnumber import OSNumber, guess_os_number
from flags import Flag

class Job:
    def __init__(self, os_file: Path, os_number: OSNumber) -> None:
        self.os_number = os_number
        self.os_file = os_file

        self.needs_layout = False
        self.needs_paper_proof = False
        self.look_for_items_to_send()

        self.files = []

    
    def __repr__(self) -> str:
        return f"{self.os_number}, layout={self.needs_layout}, proof={self.needs_paper_proof})"

    def look_for_items_to_send(self):
        
        with open(self.os_file, "rb") as file:
            
            pdf_reader = PdfFileReader(file)
            
            """
            Falta implementar o que fazer caso o PDF tenha mais de uma página.
            """
            pages = pdf_reader.pages[0]
            TEXT = pages.extract_text().split("\n")

        """
        Tirar essas constantes do código e colocar em um arquivo de config.
        """
        HEAD = "Itens para Expedir:"
        FOOT =  "Observações:"
        COMMENT = "- Com"
        PLATES = "Clichês"
        LAYOUT = "Print Layout"
        PAPER_PROOF = "Prova Digital"
        head_index = 0
        foot_index = 0

        for line in TEXT:
            if line == HEAD:
                head_index = TEXT.index(line) + 2
            elif line == FOOT:
                foot_index = TEXT.index(line)
        
        items = TEXT[head_index:foot_index]

        # Remove the comments and creat a set with unique entries.
        items = set([item for item in items if not item.startswith(COMMENT)])


        """
        Falta terminar de implementar essa parte final com o restante dos
        materiais possíveis para um Job.
        """
        for item in items:
            if item.startswith(PLATES):
                self.needs_plates = True
            elif item.startswith(LAYOUT):
                self.needs_layout = True
            elif item.startswith(PAPER_PROOF):
                self.needs_paper_proof = True
    
    def look_for_materials(self, look_up_files: list([Path])) -> list([Path]):
        """
        Iterates over a list of Pathes and looks for matching OSNumber. Returns
        the full path to the found file.
        """
        materials = []
        for file in look_up_files:
            found_os = guess_os_number(file.name)
            if found_os and found_os.number == self.os_number.number:
                materials.append(file)
        return materials
        
    
    def gather_job_files(self, source: list, destination: Path) -> None:
        if not os.path.exists(destination):
            os.mkdir(destination)
        else:
            print("Diretório já existe!")
        
        for file in source:
            copy(file, destination)
            self.files.append(destination.joinpath(file.name))
        
        print(self.files)