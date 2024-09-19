import sys
from app.Scanner import Scanner

hadError = False


def main():

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if hadError:
        exit(1)

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Uncomment this block to pass the first stage
    if file_contents:
        scanner = Scanner(file_contents)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)
    else:
        # Placeholder, remove this line when implementing the scanner
        print("EOF  null")


if __name__ == "__main__":
    main()
