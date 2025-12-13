import subprocess
from nove_error import report_error

def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        report_error(str(e))

def write_file(filepath: str, content: str):
    try:
        with open(filepath, "w") as f:
            return f.write(content)
    except Exception as e:
        report_error(str(e))

def cmd_call(cmd: list[str], silent: bool = False):
    assert type(cmd) == list

    if not silent:
        print(f"CMD: {" ".join([str(x) for x in cmd])}")

    subprocess.call(cmd)