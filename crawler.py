import os
from pathlib import Path
from datetime import date

from osnumber import OsNumber, guess_os_number
from jobs import Job
from flags import Flag


def scan_folder_for_jobs(folder: Path) -> list([Job]):
    """
    Scans a directory looking for jobs to do and returns a list with Job
    objects for the jobs found.
    """
    jobs = []
    candidates = [Path(f) for f in os.listdir(folder)]
    print("candidates:", candidates)
    for candidate in candidates:
        os_number = guess_os_number(candidate.name)
        if os_number:
            print(os_number)
            jobs.append(Job(Path(folder, candidate), os_number))
    return jobs
        

def main():
    LISTA = Path(r"E:\Desktop\Lista")
    LAYOUTS_DIR = r"F:\blumenau\Print Layout\13-06-2022"
    DIGITAIS_DIR = r"F:\blumenau\Print Digital\13-06-2022"
    destino = Path(r"E:\Desktop\Imprimir")

    JOBS_TO_DO = scan_folder_for_jobs(LISTA)
    p = input(f"Jobs to do:\n{JOBS_TO_DO}\nContine...")

    LAYOUTS = [Path(LAYOUTS_DIR, i) for i in os.listdir(LAYOUTS_DIR)]
    p = input(f"Layouts in dir:\n{LAYOUTS}\nContine...")
    DIGITAIS = [Path(DIGITAIS_DIR, i) for i in os.listdir(DIGITAIS_DIR)]
    p = input(f"Proofs in dir:\n{DIGITAIS}\nContine...")

    for job in JOBS_TO_DO:
        print(f"Processando {job.os_number}...")
        new_folder = destino.joinpath(f"{job.os_number.number}_V{job.os_number.version}")

        if job.needs_layout:
            job_layouts = job.look_for_materials(LAYOUTS)
            if job_layouts:
                job.gather_job_files(job_layouts, new_folder)
        
        if job.needs_paper_proof:
            job_proofs = job.look_for_materials(DIGITAIS)
            if job_proofs:
                job.gather_job_files(job_proofs, new_folder)
    
    p = input("Encerrar...")


if __name__ == "__main__":
    main()
