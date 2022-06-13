from pathlib import Path

from osnumber import OsNumber


class Job:
    def __init__(self, _os_num: OsNumber):
        self.os = _os_num
        self.needs_layout = False
        self.needs_proof = False
        self.layout = Path
        self.proof = Path
    
    def __repr__(self):
        return f"Job: OS {self.os.number} V{self.os.version}, layout: {self.needs_layout}, proof: {self.needs_proof}"


def look_for_items_to_send(job: Job):
    
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




def main():
    os = OsNumber(123456, 2)
    job = Job(os)
    print(job)


if __name__ == "__main__":
    main()