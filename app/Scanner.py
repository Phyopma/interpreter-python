# import TokensType as tt
from app.TokensType import TokensType as tt
from app.Token import Token
from app.error import error


class Scanner:
    keywords = {
        "and": tt.AND,
        "class": tt.CLASS,
        "else": tt.ELSE,
        "false": tt.FALSE,
        "for": tt.FOR,
        "fun": tt.FUN,
        "if": tt.IF,
        "nil": tt.NIL,
        "or": tt.OR,
        "print": tt.PRINT,
        "return": tt.RETURN,
        "super": tt.SUPER,
        "this": tt.THIS,
        "true": tt.TRUE,
        "var": tt.VAR,
        "while": tt.WHILE
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.__is_at_end():
            self.start = self.current
            self.__scan_token()

        self.tokens.append(Token(tt.EOF, "", None, self.line))
        return self.tokens

    # Character handling methods
    def __advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def __peek(self):
        if self.__is_at_end():
            return '\0'
        return self.source[self.current]

    def __peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def __match(self, expected):
        if self.__is_at_end() or self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def __is_at_end(self):
        return self.current >= len(self.source)

    # Token scanning methods
    def __scan_token(self):
        current = self.__advance()
        match current:
            case '(': self.__add_token(tt.LEFT_PAREN)
            case ')': self.__add_token(tt.RIGHT_PAREN)
            case '{': self.__add_token(tt.LEFT_BRACE)
            case '}': self.__add_token(tt.RIGHT_BRACE)
            case ',': self.__add_token(tt.COMMA)
            case '.': self.__add_token(tt.DOT)
            case '-': self.__add_token(tt.MINUS)
            case '+': self.__add_token(tt.PLUS)
            case ';': self.__add_token(tt.SEMICOLON)
            case '*': self.__add_token(tt.STAR)
            case '!': self.__add_token(tt.BANG_EQUAL if self.__match('=') else tt.BANG)
            case '=': self.__add_token(tt.EQUAL_EQUAL if self.__match('=') else tt.EQUAL)
            case '<': self.__add_token(tt.LESS_EQUAL if self.__match('=') else tt.LESS)
            case '>': self.__add_token(tt.GREATER_EQUAL if self.__match('=') else tt.GREATER)
            case '/':
                if self.__match('/'):
                    self.__skip_comment()
                else:
                    self.__add_token(tt.SLASH)
            case _ if current.isspace():
                self.__handle_whitespace(current)
            case '"':
                self.__string()
            case _:
                if current.isdigit():
                    self.__number()
                elif self.__is_alpha(current):
                    self.__identifier()
                else:
                    error(self.line, f"Unexpected character: {current}")

    # Specific token handling methods
    def __skip_comment(self):
        while self.__peek() != '\n' and not self.__is_at_end():
            self.__advance()

    def __handle_whitespace(self, current):
        if current == '\n':
            self.line += 1

    def __string(self):
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == '\n':
                self.line += 1
            self.__advance()

        if self.__is_at_end():
            error(self.line, "Unterminated string.")
            return

        self.__advance()
        value = self.source[self.start + 1:self.current - 1]
        self.__add_token(tt.STRING, value)

    def __number(self):
        while self.__peek().isdigit():
            self.__advance()

        if self.__peek() == '.' and self.__peek_next().isdigit():
            self.__advance()

            while self.__peek().isdigit():
                self.__advance()

        self.__add_token(tt.NUMBER, float(
            self.source[self.start:self.current]))

    def __identifier(self):
        while self.__is_alpha_numeric(self.__peek()):
            self.__advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, tt.IDENTIFIER)
        self.__add_token(token_type)

    # Utility methods
    def __is_alpha(self, c):
        return c.isalpha() or c == '_'

    def __is_alpha_numeric(self, c):
        return self.__is_alpha(c) or c.isdigit()

    def __add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
