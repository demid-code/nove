import sys, shutil
from pathlib import Path

from nove_error import report_error
from nove_utils import write_file, cmd_call
from nove_lexer import Lexer
from nove_parser import Parser
from nove_compiler import Compiler

def usage(program: str = None):
    print(f"Usage: {program or sys.argv[0]} <subcommand> [flags]")
    print("Subcommands:")
    print("    help                Prints usage and exits")
    print("    lex   <filepath>    Lexes source, produces and prints tokens")
    print("    parse <filepath>    Parses source, produces and prints operands")
    print("    gen   <filepath>    Generates build folder")
    print("    com   <filepath>    Generates and compiles build folder")
    print("Flags:")
    print("    -r    Runs executable after successfull compilation")
    print("    -s    Silent mode")
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

        case "lex" | "parse" | "gen" | "com":
            if len(sys.argv) < 3:
                report_error(f"Expected <filepath> for `{subcommand}` subcommand")

            nove_path = Path(__file__).parent.parent
            src_path = nove_path.joinpath("src")

            filepath = Path(sys.argv[2])
            filename = str(filepath.name).split(".")[0]

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

            build_path = filepath.parent.joinpath("build")
            build_path.mkdir(exist_ok=True)

            nove_runtime_h_path = src_path.joinpath("nove_runtime.h")
            nove_runtime_c_path = src_path.joinpath("nove_runtime.c")

            build_nove_runtime_h = build_path.joinpath("nove_runtime.h")
            build_nove_runtime_c = build_path.joinpath("nove_runtime.c")

            shutil.copyfile(nove_runtime_h_path, build_nove_runtime_h)
            shutil.copyfile(nove_runtime_c_path, build_nove_runtime_c)

            main_path = build_path.joinpath("main.c")

            compiler = Compiler(ops)
            output = compiler.compile()

            write_file(main_path, output)

            if subcommand == "gen": return

            silent_mode = "-s" in sys.argv

            exe_path = build_path.joinpath(filename)

            cmd_call(["gcc", main_path, build_nove_runtime_c, "-o", exe_path], silent_mode)
            if "-r" in sys.argv:
                cmd_call([exe_path], silent_mode)

        case _:
            usage()
            report_error(f"Invalid subcommand `{subcommand}`")

if __name__ == "__main__":
    main()