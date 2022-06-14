from dataclasses import dataclass, field
from pathlib import Path

from osnumber import OsNumber

@dataclass
class Job:
    os: OsNumber
    needs_layout: bool = False
    needs_proof: bool = False
    profile: str = ""
    pdf: Path = None

    def __repr__(self):
        return f"OS_{self.os.number}_V{self.os.version}"