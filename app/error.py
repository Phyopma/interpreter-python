import sys
from app.TokensType import TokensType as tt
from app.Token import Token

hadError = False


def error(line: int, message):
    report(line, "", message)


def getHadError():
    return hadError


def setHadError():
    global hadError
    hadError = True


def report(line, where, message):
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    setHadError()


def token_error(token: Token, message):
    if token.tokenType == tt.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)
