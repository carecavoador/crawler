import os
from pathlib import Path
from datetime import date

from osnumber import OSNumber, guess_os_number
from jobs import Job


# TODAY = date.today().strftime("%d-%m-%Y")
TODAY = "09-06-2022"
ROOT_DIR = Path(r"C:\Projetos\Python\crawler\Arquivos")
PROOFS_DIR = ROOT_DIR.joinpath("Print Digital", TODAY)
LAYOUTS_DIR = ROOT_DIR.joinpath("Print Layout", TODAY)


proof_files = os.listdir(PROOFS_DIR)
layout_files = os.listdir(LAYOUTS_DIR)
os_files = os.listdir(ROOT_DIR)


def look_for_jobs(where: list([Path])) -> list([Job]):
    """
    Lists all the files (candidates) in the given path (where) and looks for
    the os number and os version in the candidates list.
    """
    # candidates = [Path(_f) for _f in os.listdir(where)]
    
    jobs = []

    for candidate in where:
        os_number = guess_os_number(candidate.name)
        if os_number:
            jobs.append(Job(candidate, os_number))
    
    return jobs


def main():
    scan_dir = [Path(ROOT_DIR, f) for f in os.listdir(ROOT_DIR)]
    jobs_pra_fazer = look_for_jobs(scan_dir)

    layouts_list = [Path(ROOT_DIR, i) for i in os.listdir(LAYOUTS_DIR)]
    proofs_list = [Path(ROOT_DIR, i) for i in os.listdir(PROOFS_DIR)]

    for item in jobs_pra_fazer:
        print(item)
        if item.needs_layout:
            layouts = item.look_for_materials(layouts_list)
            print("\tlayout:", layouts)
        if item.needs_paper_proof:
            proofs = item.look_for_materials(proofs_list)
            print("\tproof:", proofs)
    
    pausa = input("Pressione uma tecla para encerrar.")
        

if __name__ == "__main__":
    main()
