import sys
from app.Scanner import Scanner
from app.error import getHadError, getHadRuntimeError
from app.Parser import Parser
from app.AstPrinter import AstPrinter
from app.Interpreter import Interpreter


def validate_arguments():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        print("Commands: tokenize, parse, evaluate, run", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    if command not in ["tokenize", "parse", "evaluate", "run"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    return command, sys.argv[2]


def process_file(filename):
    try:
        with open(filename) as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        exit(1)
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        exit(1)


def execute_command(command, file_contents):
    if not file_contents:
        print("EOF  null")
        return

    scanner = Scanner(file_contents)
    tokens = scanner.scan_tokens()

    if getHadError():
        exit(65)

    if command == "tokenize":
        for token in tokens:
            print(token)
        return

    parser = Parser(tokens)
    try:
        statements = parser.parse(command)
        if getHadError():
            exit(65)  # Exit immediately on syntax error
        if command == "parse":
            print(AstPrinter().print(statements))
        elif command in ["evaluate", "run"]:
            interpreter = Interpreter()
            interpreter.interpret(statements, command)
            if getHadRuntimeError():
                exit(70)  # Exit immediately on runtime error
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit(65)


def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    command, filename = validate_arguments()
    file_contents = process_file(filename)
    execute_command(command, file_contents)
    exit(0)  # Only exit with 0 if no errors occurred


if __name__ == "__main__":
    main()
