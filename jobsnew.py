from dataclasses import dataclass, field
from pathlib import Path

from PyPDF2 import PdfFileReader

from flags import Flag

@dataclass
class Job:
    os: int
    version: int
    layout: list([Path])
    proof: list([Path])
    needs_layout: bool = False
    needs_proof: bool = False


def look_for_items_to_send(os_file: Path) -> list([Flag]):
    
    with open(os_file, "rb") as file:
        
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

    result = []
    """
    Falta terminar de implementar essa parte final com o restante dos
    materiais possíveis para um Job.
    """
    for item in items:
        if item.startswith(LAYOUT):
            result.append(Flag.LAYOUT)
        elif item.startswith(PAPER_PROOF):
            result.append(Flag.PROOF)
    
    return result


def main():
    arquivo = Path(r"E:\python\crawler\Arquivos\OS_561196_2_V2.pdf")
    itens = look_for_items_to_send(arquivo)
    print(itens[0].LAYOUT)

if __name__ == "__main__":
    main()
