import sys
from app.Scanner import Scanner
from app.error import getHadError, getHadRuntimeError
from app.Parser import Parser
from app.AstPrinter import AstPrinter
from app.Interpreter import Interpreter


def validate_arguments():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        print("Commands: tokenize, parse, evaluate", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    if command not in ["tokenize", "parse", "evaluate"]:
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

    if command == "tokenize":
        for token in tokens:
            print(token)
    elif command == "parse":
        parser = Parser(tokens)
        expression = parser.parse()
        if getHadError():
            return
        print(AstPrinter().print(expression))
    elif command == "evaluate":
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(expression)


def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    command, filename = validate_arguments()
    file_contents = process_file(filename)
    execute_command(command, file_contents)

    if getHadError():
        exit(65)
    if getHadRuntimeError():
        exit(70)
    exit(0)


if __name__ == "__main__":
    main()
