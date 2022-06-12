from dataclasses import dataclass
import re

@dataclass
class OSNumber:
    number: int
    version: int
    order: int = 0

    def __repr__(self):
        if self.order:
            return f"OS {self.number} P{self.order} V{self.version}"
        else:
            return f"OS {self.number} V{self.version}"


"""
Regular expression pattern to match 4 or more digits (OS number) followed by a
version number as in '123456_v13' or 4 or more digits (OS number) followed by
a order number and a version numberin '123456_3_v9'.
"""
RE_OS = "([0-9]{4,}.[vV][0-9]+)|([0-9]{4,}.[0-9]+.[vV][0-9]+)|([0-9]{4,}.p[0-9]+.[vV][0-9]+)"

def guess_os_number(filename: str) -> OSNumber:
    """
    Tries to guess the os number, record and version from a given filename and
    returns a OSNumber object.
    """
    os_number = re.search(RE_OS, filename)
    if os_number:
        match = os_number.group().split("_")
        if len(match) == 3:
            return OSNumber(int(match[0]), int(match[1]), int(match[2][1:]))
        elif len(match) == 2:
            return OSNumber(int(match[0]), int(match[1][1:]))
        else:
            return None
    else:
        return None