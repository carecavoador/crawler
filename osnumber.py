from dataclasses import dataclass

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
