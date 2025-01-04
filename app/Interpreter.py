from app.tool import Expr, Stmt
from app.TokensType import TokensType as tt
from app.RuntimeError import RuntimeError
from app.error import runtime_error, token_error


class Interpreter(Expr.Visitor, Stmt.Visitor):

    def interpret(self, statements, command):
        try:
            if (command == "run"):
                for statement in statements:
                    self.execute(statement)
            elif (command == "evaluate"):
                value = self.evaluate(statements)
                print(self.stringify(value))
        except RuntimeError as e:
            runtime_error(e)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.tokenType == tt.MINUS:
            self.checkNumberOperand(expr.operator, right)
            return -right
        elif expr.operator.tokenType == tt.BANG:
            return not self.isTruthy(right)

        return None

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if (expr.operator.tokenType == tt.MINUS):
            self.checkNumberOperands(expr.operator, left, right)
            return left - right
        elif (expr.operator.tokenType == tt.SLASH):
            self.checkNumberOperands(expr.operator, left, right)
            return left / right
        elif (expr.operator.tokenType == tt.STAR):
            self.checkNumberOperands(expr.operator, left, right)
            return left * right
        elif (expr.operator.tokenType == tt.PLUS):
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(
                expr.operator, "Operands must be two numbers or two strings.")

        elif (expr.operator.tokenType == tt.GREATER):
            self.checkNumberOperands(expr.operator, left, right)
            return left > right
        elif (expr.operator.tokenType == tt.GREATER_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return left >= right
        elif (expr.operator.tokenType == tt.LESS):
            self.checkNumberOperands(expr.operator, left, right)
            return left < right
        elif (expr.operator.tokenType == tt.LESS_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return left <= right
        elif (expr.operator.tokenType == tt.BANG_EQUAL):
            return not self.isEqual(left, right)
        elif (expr.operator.tokenType == tt.EQUAL_EQUAL):
            return self.isEqual(left, right)
        return None

    def isEqual(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
            printf(a, b, a == b)
        return a == b

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        return stmt.accept(self)

    def isTruthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def checkNumberOperand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(
            operator, f"Operand must be a number.")

    def checkNumberOperands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, f"Operands must be numbers.")

    def stringify(self, obj):
        if obj is None:
            return "nil"
        if isinstance(obj, bool):
            return "true" if obj else "false"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)
