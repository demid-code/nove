import sys
from pathlib import Path

from nove_error import report_error
from nove_lexer import Lexer
from nove_parser import Parser

def usage(program: str = None):
    print(f"Usage: {program or sys.argv[0]} <subcommand>")
    print("Subcommands:")
    print("    help                Prints usage and exits")
    print("    lex   <filepath>    Lexes source, produces and prints tokens")
    print("    parse <filepath>    Parses source, produces and prints operands")
    print()

def main():
    if len(sys.argv) < 2:
        usage()
        report_error("No subcommand provided")

    subcommand = sys.argv[1]

    match subcommand:
        case "help":
            usage()
            return

        case "lex" | "parse":
            if len(sys.argv) < 3:
                report_error(f"Expected <filepath> for `{subcommand}` subcommand")

            filepath = Path(sys.argv[2])
            lexer = Lexer(filepath)
            tokens = lexer.lex()
            if len(tokens) <= 0: return

            if subcommand == "lex":
                for token in tokens:
                    print(token)
                return

            parser = Parser(tokens)
            ops = parser.parse()
            if len(ops) <= 0: return

            if subcommand == "parse":
                for i, op in enumerate(ops):
                    print(f"{i}: {op}")
                return

        case _:
            usage()
            report_error(f"Invalid subcommand `{subcommand}`")

if __name__ == "__main__":
    main()