import os
import json
from sys import argv
from pathlib import Path
from shutil import move, copy
from datetime import date, datetime

from osnumber import OSNumber, guess_os_number
from jobs import Job
from juntapdf.juntapdf import merge_pdfs


def load_config(config_file: str) -> dict:
    try:
        return json.load(open(config_file, "r", encoding="utf-8"))
    except FileNotFoundError:
        print("Arquivo de configuração não encontrado.")
        config = {}
        config["jobs_folder"] = input(r"Localização da pasta de Entrada: ")
        config["output_folder"] = input(r"Localização da pasta de Saída: ")
        config["layouts_folder"] = input(r"Localização da pasta de Prints Layout: ")
        config["proofs_folder"] = input(r"Localização da pasta de Provas Digitais: ")
    
        with open(Path(__file__).parent.joinpath(config_file), "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)
        
        return config


def scan_folder_for_jobs(location: Path) -> list[Job]:
    """
    Scans a directory looking for jobs to do and returns a list with Job
    objects with the jobs found.
    """
    found_jobs = []
    candidates = [Path(location, f) for f in os.listdir(location)]

    for candidate in candidates:
        os_num = guess_os_number(candidate.name)
        if os_num:
            found_jobs.append(
                Job(os_num, candidate)
            )
    return found_jobs


def os_match(job: Job, os: OSNumber) -> bool:
    """Compares if a OSNumber is equal to a Job's OSNumber."""
    if job.os.number == os.number and job.os.version == os.version:
        return True
    else:
        return False


def find_job_files(job: Job, location: Path) -> list[Path]:
    """
    Tries to find Job files in a specific directory and returns a list
    of Path objects with the full path to the found files.
    """
    job_files = []

    files = os.listdir(location)
    files = [Path(location, file) for file in files]

    for file in files:
        # Checks for OSNumber in filename.
        os_num = guess_os_number(file.name)

        # Append file to job_files if OsNumbers match.
        if os_num and os_match(job, os_num):
            job_files.append(file)
    
    return job_files


def prompt_user(prompt: str, choices: list) -> str:
    while True:
        print(prompt)
        choice = input("> ").lower()
        if choice in choices:
            return choice
        print("Opção inválida.")


def retreive_job_files(job: Job, location: Path, output: Path, description: str ="") -> int:

    found_files = find_job_files(job, location)
    files_done = 0

    for file in found_files:
        copy(file, output.joinpath(f"{job}{description}{file.suffix}"))
        files_done += 1
        done_dir = location.joinpath("Baixados")
        
        if not done_dir.exists():
            os.mkdir(done_dir)
        
        try:
            move(file, done_dir)
        except FileExistsError:
            overwrite = prompt_user(f"-> ATENÇÃO! O arquivo {file.name} já foi baixado. Deseja substituí-lo? (esta ação não poderá ser desfeita!) Sim/Não?", ["sim", "s", "nao", "n", "não"])
            if overwrite == "sim" or overwrite == "s":
                copy(file, done_dir)
                os.remove(file)
                print(f"--> O arquivo {file.name} FOI substituído.")
            else:
                print(f"--> O arquivo {file.name} NÃO foi substituído.")

    return files_done


def work(jobs: list[Job], layouts_dir: Path, proofs_dir: Path, output_dir: Path) -> None:
    
    for job in jobs:
        print(f"> Processando {job}...")

        # Job needs layout.
        if job.needs_layout:
            output_layouts = output_dir.joinpath("Prints Layout")

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
            output_proofs = output_dir.joinpath("Provas Digitais")

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
    ROOT_FOLDER = Path(__file__).parent
    # -------------------------------------------------------------------------
    # Reads options and arguments passed by the CLI if any.
    options = [opt for opt in argv[1:] if opt.startswith("--")]
    arguments = [arg for arg in argv[1:] if not arg.startswith("--")]

    if "--config" in options:
        # Defines a config file passed as a CLI argument with the --config option.
        opt_index = argv.index("--config")
        CONFIG = load_config(argv[opt_index+1])
    else:
        # If no optional config file is passed via CLI, uses the default.
        CONFIG = load_config(ROOT_FOLDER.joinpath("config.json"))

    if "--greet" in options:
        # This is just a joke to test positional options and arguments. Delete this!
        opt_index = argv.index("--greet")
        greet = argv[opt_index+1]
        print(f"Seja bem vindo, mestre {greet}!")

    TODAY = date.today().strftime("%d-%m-%Y")
    NOW = datetime.now().strftime("%H-%M-%S")
    JOBS_FOLDER = Path(CONFIG["jobs_folder"])
    OUTPUT_FOLDER = Path(CONFIG["output_folder"])
    LAYOUTS_FOLDER = Path(CONFIG["layouts_folder"], TODAY)
    PROOFS_FOLDER = Path(CONFIG["proofs_folder"], TODAY)
    # -------------------------------------------------------------------------

    jobs_to_do = scan_folder_for_jobs(JOBS_FOLDER)
    
    if jobs_to_do:
        print(f"> {len(jobs_to_do)} Jobs encontrados:", jobs_to_do)

        work(jobs_to_do, LAYOUTS_FOLDER, PROOFS_FOLDER, OUTPUT_FOLDER)
        missing_layouts = [job for job in jobs_to_do if job.needs_layout]
        missing_proofs = [job for job in jobs_to_do if job.needs_proof]

        if missing_layouts:
            print("> Não encontrei os Layouts para:", missing_layouts)

        if missing_proofs:
            print("> Não encontrei as Provas Digitais para:", missing_proofs)

        if len(jobs_to_do) > 1:
            # Junta os PDFs das OS em um único arquivo para impressão.
            merge_pdfs([job.pdf for job in jobs_to_do],JOBS_FOLDER.joinpath("OS_juntas_" + NOW + ".pdf"))

        print("Terminei de trabalhar. Agora é sua vez!")
    
    else:
        print("Não tem trabalhos pra fazer. Vai pegar um café...")



if __name__ == "__main__":
    main()

    # Fim do programa.
    print("Programa terminado.")
