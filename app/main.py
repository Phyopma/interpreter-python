import sys
from app.Scanner import Scanner
from app.error import getHadError, hadError
from app.Parser import Parser
from app.AstPrinter import AstPrinter


def main():

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if not command in ["tokenize", "parse"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

        if file_contents:
            scanner = Scanner(file_contents)
            tokens = scanner.scan_tokens()
            if command == "tokenize":
                for token in tokens:
                    print(token)
            elif command == "parse":
                parser = Parser(tokens)
                expression = parser.parse()

                if getHadError():
                    exit(1)

                print(AstPrinter().print(expression))

        else:
            print("EOF  null")

    if getHadError():
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
