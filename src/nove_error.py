import sys
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Loc:
    filepath: Path
    line: int
    col: int

    def copy(self):
        return Loc(self.filepath, self.line, self.col)

    def __repr__(self) -> str:
        return f"{self.filepath}:{self.line}:{self.col}"

def report_error(msg: str, loc: Loc = None):
    if loc != None:
        print(f"{loc}: Error: {msg}", file=sys.stderr)
    else:
        print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)