from app.TokensType import TokensType as tt
from app.tool import Expr, Stmt
from app.error import token_error, runtime_error
from app.RuntimeError import RuntimeError


class Parser:
    class ParseError(Exception):
        pass

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self, command):
        try:
            if command == "run":
                statements = []
                while (not self.is_at_end()):
                    statements.append(self.declaration())
                return statements
            return self.expression()
        except RuntimeError as e:
            runtime_error(e)
            return None
        except Parser.ParseError:
            return None

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.OR()

        if self.match(tt.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def OR(self):
        expr = self.AND()

        while self.match(tt.OR):
            operator = self.previous()
            right = self.AND()
            expr = Expr.Logical(expr, operator, right)

        return expr

    def AND(self):
        expr = self.equality()

        while self.match(tt.AND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)

        return expr

    def declaration(self):
        try:
            if self.match(tt.FUN):
                return self.function("function")
            if self.match(tt.VAR):
                return self.var_declaration()
            return self.statement()
        except Parser.ParseError:
            self.synchronize()
            return None

    def statement(self):
        if self.match(tt.FOR):
            return self.for_statement()
        if self.match(tt.IF):
            return self.if_statement()
        if self.match(tt.PRINT):
            return self.print_statement()
        if self.match(tt.WHILE):
            return self.while_statement()
        if self.match(tt.LEFT_BRACE):
            return Stmt.Block(self.block())
        return self.expression_statement()

    def for_statement(self):
        self.consume(tt.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer = None
        if self.match(tt.SEMICOLON):
            initializer = None
        elif self.match(tt.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(tt.SEMICOLON):
            condition = self.expression()
        self.consume(tt.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(tt.RIGHT_PAREN):
            increment = self.expression()
        self.consume(tt.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()

        if increment is not None:
            body = Stmt.Block([body, Stmt.Expression(increment)])
        if condition is None:
            condition = Expr.Literal(True)
        body = Stmt.While(condition, body)
        if initializer is not None:
            body = Stmt.Block([initializer, body])

        return body

    def while_statement(self):
        self.consume(tt.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(tt.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return Stmt.While(condition, body)

    def if_statement(self):
        self.consume(tt.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(tt.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(tt.ELSE):
            else_branch = self.statement()

        return Stmt.If(condition, then_branch, else_branch)

    def print_statement(self):
        value = self.expression()
        self.consume(tt.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def var_declaration(self):
        name = self.consume(tt.IDENTIFIER, "Expect variable name.")

        intializer = None
        if self.match(tt.EQUAL):
            intializer = self.expression()

        self.consume(tt.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, intializer)

    def function(self, kind):
        name = self.consume(tt.IDENTIFIER, f"Expect {kind} name.")
        self.consume(tt.LEFT_PAREN, f"Expect '(' after {kind} name.")
        paramenters = []
        if not self.check(tt.RIGHT_PAREN):
            paramenters.append(self.consume(
                tt.IDENTIFIER, "Expect parameter name."))
            while self.match(tt.COMMA):
                if len(paramenters) >= 255:
                    self.error(
                        self.peek(), "Cannot have more than 255 parameters.")
                paramenters.append(self.consume(
                    tt.IDENTIFIER, "Expect parameter name."))
        self.consume(tt.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(tt.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()
        return Stmt.Function(name, paramenters, body)

    def expression_statement(self):
        expr = self.expression()
        self.consume(tt.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def block(self):
        statements = []

        while not self.check(tt.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(tt.RIGHT_BRACE, "Expect '}' after block.")

        return statements

    def equality(self):
        expr = self.comparison()

        while self.match(tt.BANG_EQUAL, tt.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        if type == tt.SEMICOLON:
            raise RuntimeError(self.peek(), message)
        raise self.error(self.peek(), message)

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().tokenType == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().tokenType == tt.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        token_error(token, message)
        return Parser.ParseError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == tt.SEMICOLON:
                return

            if self.peek().type in [tt.CLASS, tt.FUN, tt.VAR, tt.FOR, tt.IF, tt.WHILE, tt.PRINT, tt.RETURN]:
                return

            self.advance()

    def comparison(self):
        expr = self.term()

        while self.match(tt.GREATER, tt.GREATER_EQUAL, tt.LESS, tt.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(tt.MINUS, tt.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(tt.SLASH, tt.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(tt.BANG, tt.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.call()

    def call(self):
        expr = self.primary()

        while True:
            if self.match(tt.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        return expr

    def finish_call(self, callee):
        arguments = []

        if not self.check(tt.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(tt.COMMA):
                if len(arguments) >= 255:
                    self.error(
                        self.peek(), "Cannot have more than 255 arguments.")
                arguments.append(self.expression())

        paren = self.consume(tt.RIGHT_PAREN, "Expect ')' after arguments.")

        return Expr.Call(callee, paren, arguments)

    def primary(self):
        if self.match(tt.FALSE):
            return Expr.Literal(False)
        if self.match(tt.TRUE):
            return Expr.Literal(True)
        if self.match(tt.NIL):
            return Expr.Literal(None)

        if self.match(tt.NUMBER, tt.STRING):
            return Expr.Literal(self.previous().literal)

        if self.match(tt.IDENTIFIER):
            return Expr.Variable(self.previous())

        if self.match(tt.LEFT_PAREN):
            expr = self.expression()
            self.consume(tt.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")
