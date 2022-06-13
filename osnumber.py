from dataclasses import dataclass
import re

@dataclass
class OsNumber:
    number: int
    version: int

"""
Regular expression pattern to match 4 or more digits (OS Number) followed by
any character or space and version number as in '123456_v13'.
"""
# RE_OS = "(\d{4,}).[vV](\d+)|(\d{4,})_\d+_[vV](\d+)"
RE_OS = "(\d{4,}).*[vV](\d+)"

def guess_os_number(filename: str) -> OsNumber:
    """
    Tries to guess the OS Number and version from a given filename and returns
    an 'OsNumber' object. Returns 'None' if no Os Number is found.
    """
    _os_number = re.search(RE_OS, filename)
    if _os_number:
        n = _os_number.group(1)
        v = _os_number.group(2)
        return OsNumber(n, v)
    else:
        return None
