import sys


def error(line, message):
    report(line, "", message)


def report(line, where, message):
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    had_error = True
