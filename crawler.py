import os
import re
from pathlib import Path
from shutil import move, copy
from datetime import date, datetime
from timeit import timeit

from PyPDF2 import PdfFileReader

from osnumber import OsNumber, guess_os_number
from jobs import Job
from juntapdf import juntapdf
from logger import logger as log

TODAY = date.today().strftime("%d-%m-%Y")
AGORA = datetime.now().strftime("%H-%M-%S")
DESKTOP = Path(os.path.expanduser("~/Desktop"))
# ENTRADA = Path(r"E:\Desktop")
ENTRADA = Path(DESKTOP, "Entrada")
SAIDA = Path(DESKTOP, "Saida")
# SAIDA = Path(r"X:\Transporte\Leticia") # Saída Letícia
LAYOUTS = Path(r"F:\blumenau\Print Layout").joinpath(TODAY)
DIGITAIS = Path(r"F:\blumenau\Print Digital").joinpath(TODAY)


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

    return (profile, layout, proof, pdf)


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
            new_job.pdf = job_data[3]
            jobs.append(new_job)
    
    return jobs


def retreive_job_files(job: Job, origin: Path, output: Path, description: str ="") -> int():
    found_files = find_job_files(job, origin)
    files_done = 0
    if found_files:
        for file in found_files:
            copy(file, output.joinpath(f"{job}{description}{file.suffix}"))
            files_done += 1
            done_dir = origin.joinpath("Baixados")
            if not done_dir.exists():
                os.mkdir(done_dir)
            try:
                move(file, done_dir)
            except Exception as e:
                print(e)
    return files_done


def work(jobs: list([Job]), layouts_dir: Path, proofs_dir: Path, destination: Path) -> None:
    for i, job in enumerate(jobs):
        print(f"{i} Processando {job}...")

        # Job needs layout.
        if job.needs_layout:
            output_layouts = destination.joinpath("Prints Layout")

            # Checks if output dir exists. If not, create it.
            if not output_layouts.exists():
                os.mkdir(output_layouts)
            
            layouts_done = retreive_job_files(
                job=job,
                origin=layouts_dir,
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
                origin=proofs_dir,
                output=output_proofs,
                description=job.profile
            )
            if proofs_done:
                job.needs_proof = False


def main():
    jobs_to_do = scan_folder_for_jobs(ENTRADA)
    if jobs_to_do:
        print(f"Jobs encontrados ({len(jobs_to_do)}):", jobs_to_do)

        work(jobs_to_do, LAYOUTS, DIGITAIS, SAIDA)

        missing_layouts = [job for job in jobs_to_do if job.needs_layout]
        missing_proofs = [job for job in jobs_to_do if job.needs_proof]
        if missing_layouts:
            print("Não encontrei os Layouts para:", missing_layouts)

        if missing_proofs:
            print("Não encontrei as Provas Digitais para:", missing_proofs)
    else:
        print("Não tem trabalhos pra fazer. Vai pegar um café...")
        input("Pressione qualquer tecla para sair.")
        quit()

    # Junta os PDFs das OS em um único arquivo para impressão.
    juntapdf.merge_pdfs(
        [job.pdf for job in jobs_to_do],
        ENTRADA.joinpath("OS_juntas_" + AGORA + ".pdf")
        )

    # Fim do programa.
    prinint("Terminei de trabalhar. Agora é sua vez!")
    input("Pressione qualquer tecla para sair.")
    log.logger.info("Executou com sucesso ", AGORA)


if __name__ == "__main__":
    main()
