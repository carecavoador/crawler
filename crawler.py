import os
import re
from pathlib import Path
from shutil import move, copy
from datetime import date

from PyPDF2 import PdfFileReader

from osnumber import OsNumber, guess_os_number
from jobs import Job

TODAY = date.today().strftime("%d-%m-%Y")
ENTRADA = Path(r"E:\Desktop\Entrada")
LAYOUTS = Path(r"F:\blumenau\Print Layout").joinpath(TODAY)
DIGITAIS = Path(r"F:\blumenau\Print Digital").joinpath(TODAY)
SAIDA = Path(r"E:\Desktop\Saida")


def os_match(job: Job, os: OsNumber) -> bool():
    """Compares if a OsNumber is equal to a Job's OsNumber."""
    if job.os.number == os.number and job.os.version == os.version:
        return True
    else:
        return False


def find_job_files(job: Job, origin: Path) -> list([Path]):
    """
    Tries to find Job files in a specific directory and returns a list
    of Path objects with the full path to the found files.
    """
    job_files = []

    files = os.listdir(origin)
    files = [Path(origin, file) for file in files]

    for file in files:
        # Checks for OsNumber in filename.
        os_num = guess_os_number(file.name)

        # Append file to job_files if OsNumbers match.
        if os_num and os_match(job, os_num):
            job_files.append(file)
    
    return job_files


def get_data_for_job(pdf: Path) -> tuple():
    """
    Reads a PDF file and extract it's text to look for the job
    information. Returns a tuple containing: (profile: str, layout: bool,
    proof: bool).
    """
    profile = ""
    layout = False
    proof = False
    
    with open(pdf, "rb") as f:
        reader = PdfFileReader(f)
        page_one = reader.pages[0]
        text = page_one.extract_text().split("\n")
    
    for line in text:
        if line == text[14]:
            profile = "_Perfil_"
            profile += re.search("(.+)Fechamento:", line).groups(1)[0]
        elif line.startswith("Print Layout"):
            layout = True
        elif line.startswith("Prova Digital"):
            proof = True
    
    return (profile, layout, proof)


def scan_folder_for_jobs(folder: Path) -> list([Job]):
    """
    Scans a directory looking for jobs to do and returns a list with Job
    objects for the jobs found.
    """
    jobs = []
    candidates = [Path(folder, c) for c in os.listdir(folder)]

    for candidate in candidates:
        os_num = guess_os_number(candidate.name)
        if os_num:
            new_job = Job(os_num)

            job_data = get_data_for_job(candidate)
            
            new_job.profile = job_data[0]
            new_job.needs_layout = job_data[1]
            new_job.needs_proof = job_data[2]
            
            jobs.append(new_job)
    
    return jobs


def gather_files_for_job(job: Job, origin: Path(), output: Path(), description: str ="") -> int():
    found_files = find_job_files(job, origin)
    files_done = 0
    if found_files:
        for file in found_files:
            copy(file, output.joinpath(f"{job}{description}{file.suffix}"))
            files_done += 1
            done_dir = origin.joinpath("Baixados")
            if not done_dir.exists():
                os.mkdir(done_dir)
            move(file, done_dir)
    return files_done


def work(jobs: list([Job]), layouts_dir: Path(), proofs_dir: Path(), destination: Path()) -> None:
    for job in jobs:
        print(f"Processando {job}...")

        # Job needs layout.
        if job.needs_layout:
            output_layouts = destination.joinpath("Layouts")

            # Checks if output dir exists. If not, create it.
            if not output_layouts.exists():
                os.mkdir(output_layouts)
            
            layouts_done = gather_files_for_job(
                job=job,
                origin=layouts_dir,
                output=output_layouts,
                description="_Print_Layout"
            )
            if layouts_done:
                print(f"{layouts_done} layouts processados.")
            else:
                print(f"Não foi possível localizar layouts para {job}.")

        # Job needs proof.
        if job.needs_proof:
            output_proofs = destination.joinpath("Provas Digitais")

            # Checks if output dir exists. If not, create it.
            if not output_proofs.exists():
                os.mkdir(output_proofs)
            
            layouts_done = gather_files_for_job(
                job=job,
                origin=proofs_dir,
                output=output_proofs,
                description=job.profile
            )
            if layouts_done:
                print(f"{layouts_done} provas digitais processadas.")
            else:
                print(f"Não foi possível localizar provas digitais para {job}.")


def main():
    jobs_to_do = scan_folder_for_jobs(ENTRADA)
    if jobs_to_do:
        work(jobs_to_do, LAYOUTS, DIGITAIS, SAIDA)
    else:
        print("No jobs to do. Go get a coffee...")


if __name__ == "__main__":
    main()
