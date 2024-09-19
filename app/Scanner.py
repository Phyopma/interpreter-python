# import TokensType as tt
from app.TokensType import TokensType as tt
from app.Token import Token
from app.error import error


class Scanner:
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

    def __is_at_end(self):
        return self.current >= len(self.source)

    def __scan_token(self):
        current = self.__advance()
        if (current == '('):
            self.__add_token(tt.LEFT_PAREN)
        elif (current == ')'):
            self.__add_token(tt.RIGHT_PAREN)
        elif (current == '{'):
            self.__add_token(tt.LEFT_BRACE)
        elif (current == '}'):
            self.__add_token(tt.RIGHT_BRACE)
        elif (current == ','):
            self.__add_token(tt.COMMA)
        elif (current == '.'):
            self.__add_token(tt.DOT)
        elif (current == '-'):
            self.__add_token(tt.MINUS)
        elif (current == '+'):
            self.__add_token(tt.PLUS)
        elif (current == ';'):
            self.__add_token(tt.SEMICOLON)
        elif (current == '*'):
            self.__add_token(tt.STAR)
        elif (current == '!'):
            self.__add_token(tt.BANG_EQUAL if self.__match('=') else tt.BANG)
        elif (current == '='):
            self.__add_token(tt.EQUAL_EQUAL if self.__match('=') else tt.EQUAL)
        elif (current == '<'):
            self.__add_token(tt.LESS_EQUAL if self.__match('=') else tt.LESS)
        elif (current == '>'):
            self.__add_token(
                tt.GREATER_EQUAL if self.__match('=') else tt.GREATER)
        elif (current == '/'):
            if self.__match('/'):
                while self.__peek() != '\n' and not self.__is_at_end():
                    self.__advance()
            else:
                self.__add_token(tt.SLASH)
        elif (current in [' ', '\r', '\t']):
            pass
        elif (current == '\n'):
            self.line += 1
        else:
            error(self.line, "Unexpected character: " + current)

    def __advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def __add_token(self, token_type):
        self.__add_token_(token_type, None)

    def __add_token_(self, token_type, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def __match(self, expected):
        if self.__is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def __peek(self):
        if self.__is_at_end():
            return '\0'
        return self.source[self.current]
