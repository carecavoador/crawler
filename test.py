import os
from pathlib import Path
import re

from PyPDF2 import PdfFileReader

from osnumber import OsNumber, guess_os_number
from jobsnew import Job


def get_data_for_job(pdf: Path) -> tuple:
    """
    Reads a PDF file and extract it's text to look for the job information.
    Returns a tuple containing: (profile: str, layout: bool, proof: bool).
    """
    profile = ""
    layout = False
    proof = False
    
    with open(pdf, "rb") as f:
        reader = PdfFileReader(f)
        page_one = reader.pages[0]
        text = page_one.extract_text().split("\n")
    
    for n, line in enumerate(text):
        # print(n, line)
        if line == text[14]:
            profile = re.search("(.+)Fechamento:", line).groups(1)[0]
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



pasta = r"E:\Desktop\Lista"

jobs = scan_folder_for_jobs(pasta)
print(jobs)
