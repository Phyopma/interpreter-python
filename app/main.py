import sys
from app.Scanner import Scanner
from app.error import getHadError, getHadRuntimeError
from app.Parser import Parser
from app.AstPrinter import AstPrinter
from app.Interpreter import Interpreter


class CommandExecutor:
    def __init__(self, command, file_contents):
        self.command = command
        self.file_contents = file_contents
        self.scanner = Scanner(file_contents)
        self.tokens = None
        self.parser = None
        self.interpreter = None

    def execute(self):
        if not self.file_contents:
            print("EOF  null")
            return 0

        self.tokens = self.scanner.scan_tokens()
        if self.command == "tokenize":
            return self.handle_tokenize()

        return self.handle_parse_and_interpret()

    def handle_tokenize(self):
        for token in self.tokens:
            print(token)
        return 65 if getHadError() else 0

    def handle_parse_and_interpret(self):
        try:
            self.parser = Parser(self.tokens)
            statements = self.parser.parse(self.command)

            if getHadError():
                return 65

            if self.command == "parse":
                print(AstPrinter().print(statements))
            elif self.command in ["evaluate", "run"]:
                self.interpreter = Interpreter()
                self.interpreter.interpret(statements, self.command)
                if getHadRuntimeError():
                    return 70
            return 0
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return 65


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


def main():
    print("Logs from your program will appear here!", file=sys.stderr)
    command, filename = validate_arguments()
    file_contents = process_file(filename)

    executor = CommandExecutor(command, file_contents)
    exit_code = executor.execute()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
