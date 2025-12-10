from nove_error import report_error

def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        report_error(str(e))