import sys

hadError = False


def error(line, message):
    report(line, "", message)


def getHadError():
    return hadError


def setHadError():
    global hadError
    hadError = True


def report(line, where, message):
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    setHadError()
