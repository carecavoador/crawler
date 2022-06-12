import os
import re
from pathlib import Path
from datetime import date

from osnumber import OSNumber


# TODAY = date.today().strftime("%d-%m-%Y")
TODAY = "09-06-2022"
ROOT_DIR = Path(r"C:\Projetos\Python\crawler\Arquivos")
PROOFS_DIR = ROOT_DIR.joinpath("Print Digital", TODAY)
LAYOUTS_DIR = ROOT_DIR.joinpath("Print Layout", TODAY)

"""
Regular expression pattern to match 4 or more digits (OS number) followed by a
version number as in '123456_v13' or 4 or more digits (OS number) followed by
a order number and a version numberin '123456_3_v9'.
"""
RE_OS = "([0-9]{4,}.[vV][0-9]+)|([0-9]{4,}.[0-9]+.[vV][0-9]+)|([0-9]{4,}.p[0-9]+.[vV][0-9]+)"


proof_files = os.listdir(PROOFS_DIR)
layout_files = os.listdir(LAYOUTS_DIR)
os_files = os.listdir(ROOT_DIR)

def guess_os_number(filename: str) -> OSNumber:
    """
    Tries to guess the os number, record and version from a given filename and
    returns a OSNumber object.
    """
    os_number = re.search(RE_OS, filename)
    if os_number:
        match = os_number.group().split("_")
        if len(match) == 3:
            return OSNumber(int(match[0]), int(match[1]), int(match[2][1:]))
        elif len(match) == 2:
            return OSNumber(int(match[0]), int(match[1][1:]))
        else:
            return None
    else:
        return None

def look_for_job(where: Path, job: OSNumber) -> Path:
    """
    Lists all the files (candidates) in the given path (where) and looks for
    the os number and os version in the candidates list.
    """
    candidates = [Path(_f) for _f in os.listdir(where)]
    search = f"{job.number}.[vV]{job.version}"
    for candidate in candidates:
        match = re.search(search, candidate.name)
        if match:
            return candidate
    return None

def main():
    teste = [Path(f) for f in os.listdir(ROOT_DIR)]
    lista_de_os = [
        guess_os_number(item.name) for item in teste if guess_os_number(item.name)
    ]
    for job in lista_de_os:
        print(f"{job} job localizado.")
        print_layout = look_for_job(LAYOUTS_DIR, job)
        if print_layout:
            print("\tPrint layout encontrada:", print_layout)
        else:
            print("\tPrint layout não localizada.")
        prova_digital = look_for_job(PROOFS_DIR, job)
        if prova_digital:
            print("\tProva digital encontrada:", prova_digital)
        else:
            print("\tProva digital não localizada.")


if __name__ == "__main__":
    main()
