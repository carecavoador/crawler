import os
from pathlib import Path
from datetime import date

from osnumber import OSNumber, guess_os_number
from jobs import Job
from flags import Flag


# TODAY = date.today().strftime("%d-%m-%Y")
TODAY = "09-06-2022"
# DESKTOP = Path(os.path.expanduser("~/Desktop"))
DESKTOP = Path(r"C:\Users\erodr\OneDrive\Desktop")
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
    jobs = []
    for candidate in where:
        os_number = guess_os_number(candidate.name)
        if os_number:
            jobs.append(Job(candidate, os_number))
    return jobs


def main():
    scan_jobs_dir = [Path(ROOT_DIR, f) for f in os.listdir(ROOT_DIR)]
    scan_layouts_dir = [Path(LAYOUTS_DIR, i) for i in os.listdir(LAYOUTS_DIR)]
    print(scan_layouts_dir)
    scan_proofs_dir = [Path(PROOFS_DIR, i) for i in os.listdir(PROOFS_DIR)]
    print(scan_proofs_dir)

    jobs_to_do = look_for_jobs(scan_jobs_dir)

    for job in jobs_to_do:
        print(job)
        new_folder = DESKTOP.joinpath(f"{job.os_number.number}_V{job.os_number.version}")
        if job.needs_layout:
            layouts = job.look_for_materials(scan_layouts_dir)
            print("\tlayouts:", layouts)
            if layouts:
                job.gather_job_files(layouts, new_folder)
        if job.needs_paper_proof:
            proofs = job.look_for_materials(scan_proofs_dir)
            print("\tproofs:", proofs)
            if proofs:
                job.gather_job_files(proofs, new_folder)
    
    pausa = input("Pressione uma tecla para encerrar.")
        

if __name__ == "__main__":
    main()
