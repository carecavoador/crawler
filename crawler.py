import os
import re
import json
from typing import List, Tuple
from pathlib import Path
from shutil import move, copy
from datetime import date, datetime
from timeit import timeit

from PyPDF2 import PdfFileReader

from osnumber import OsNumber, guess_os_number
from jobs import Job
from juntapdf import juntapdf


# -> Configuration
TODAY = date.today().strftime("%d-%m-%Y")
NOW = datetime.now().strftime("%H-%M-%S")

# Loads config.json file and set configuration constants.
CONFIG = json.load(open("C:\Projetos\Python\crawler\config.json", "r", encoding="utf-8"))
JOBS_FOLDER = Path(CONFIG["jobs_folder"])
OUTPUT_FOLDER = Path(CONFIG["output_folder"])
LAYOUTS_FOLDER = Path(CONFIG["layouts_folder"])
PROOFS_FOLDER = Path(CONFIG["proofs_folder"])
# -----------------------------------------------------------------------------

def scan_folder_for_jobs(location: Path) -> List[Job]:
    """
    Scans a directory looking for jobs to do and returns a list with Job
    objects with the jobs found.
    """
    found_jobs = []
    candidates = [Path(location, _) for _ in os.listdir(location)]

    for candidate in candidates:
        os_num = guess_os_number(candidate.name)
        if os_num:
            profile, layout, proof, pdf = get_data_for_job(candidate)
            found_jobs.append(
                Job(
                    os=os_num,
                    profile=profile,
                    needs_layout=layout,
                    needs_proof=proof,
                    pdf=pdf
                )
            )
    return found_jobs


def os_match(job: Job, os: OsNumber) -> bool:
    """Compares if a OsNumber is equal to a Job's OsNumber."""
    if job.os.number == os.number and job.os.version == os.version:
        return True
    else:
        return False


def find_job_files(job: Job, location: Path) -> List[Path]:
    """
    Tries to find Job files in a specific directory and returns a list
    of Path objects with the full path to the found files.
    """
    job_files = []

    files = os.listdir(location)
    files = [Path(location, file) for file in files]

    for file in files:
        # Checks for OsNumber in filename.
        os_num = guess_os_number(file.name)

        # Append file to job_files if OsNumbers match.
        if os_num and os_match(job, os_num):
            job_files.append(file)
    
    return job_files


def get_data_for_job(pdf: Path) -> Tuple:
    """
    Reads a PDF file and extract it's text to look for the job
    information. Returns a tuple containing: (profile: str, layout: bool,
    proof: bool, pdf: Path).
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

    return (profile, layout, proof, pdf)


def ask_to_overwrite(file: Path) -> bool:
    choice = input(
        f"\t-> ATENÇÃO! O arquivo {file.name} já foi baixado. Deseja substituí-lo? (esta ação não poderá ser desfeita!) Sim/Não? "
    ).lower()
    
    if choice == "s" or choice == "sim":
        return True
    else:
        return False


def retreive_job_files(
        job: Job, location: Path, output: Path, description: str =""
    ) -> int:

    found_files = find_job_files(job, location)
    files_done = 0

    for file in found_files:
        copy(file, output.joinpath(f"{job}{description}{file.suffix}"))
        files_done += 1
        done_dir = location.joinpath("Baixados")
        if not done_dir.exists():
            os.mkdir(done_dir)
        
        if not file.exists():
            move(file, done_dir)
        else:
            overwrite = ask_to_overwrite(file)
            if overwrite:
                copy(file, done_dir)
                os.remove(file)
                print(f"\t--> O arquivo {file.name} FOI substituído.")
            else:
                print(f"\t--> O arquivo {file.name} NÃO foi substituído.")
    return files_done


def work(
        jobs: List[Job], layouts_dir: Path, proofs_dir: Path, destination: Path
    ) -> None:
    
    for job in jobs:
        print(f"\n\t-> Processando {job}...")

        # Job needs layout.
        if job.needs_layout:
            output_layouts = destination.joinpath("Prints Layout")

            # Checks if output dir exists. If not, create it.
            if not output_layouts.exists():
                os.mkdir(output_layouts)
            
            layouts_done = retreive_job_files(
                job=job,
                location=layouts_dir,
                output=output_layouts,
                description="_Print_Layout"
            )
            if layouts_done:
                job.needs_layout = False

        # Job needs proof.
        if job.needs_proof:
            output_proofs = destination.joinpath("Provas Digitais")

            # Checks if output dir exists. If not, create it.
            if not output_proofs.exists():
                os.mkdir(output_proofs)
            
            proofs_done = retreive_job_files(
                job=job,
                location=proofs_dir,
                output=output_proofs,
                description=job.profile
            )
            if proofs_done:
                job.needs_proof = False


def main():
    jobs_to_do = scan_folder_for_jobs(JOBS_FOLDER)
    
    if jobs_to_do:
        print(f"{len(jobs_to_do)} Jobs encontrados:", jobs_to_do)

        work(jobs_to_do, LAYOUTS_FOLDER, PROOFS_FOLDER, OUTPUT_FOLDER)
        missing_layouts = [job for job in jobs_to_do if job.needs_layout]
        missing_proofs = [job for job in jobs_to_do if job.needs_proof]

        if missing_layouts:
            print("Não encontrei os Layouts para:", missing_layouts)

        if missing_proofs:
            print("Não encontrei as Provas Digitais para:", missing_proofs)
        print("Terminei de trabalhar. Agora é sua vez!")
    
    else:
        print("Não tem trabalhos pra fazer. Vai pegar um café...")

    # Junta os PDFs das OS em um único arquivo para impressão.
    juntapdf.merge_pdfs(
        [job.pdf for job in jobs_to_do],
        JOBS_FOLDER.joinpath("OS_juntas_" + NOW + ".pdf")
    )


if __name__ == "__main__":
    main()

    # Fim do programa.
    input("Pressione qualquer tecla para sair.")
