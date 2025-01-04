from app.tool import Expr, Stmt
from app.TokensType import TokensType as tt
from app.RuntimeError import RuntimeError
from app.error import runtime_error
from app.Environment import Environment


class Interpreter(Expr.Visitor, Stmt.Visitor):

    def __init__(self):
        self.environment = Environment()

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

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
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

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name.lexeme)

    def checkType(self, value, expected_type, operator, message):
        if isinstance(value, expected_type):
            return True
        raise RuntimeError(operator, message)

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        type_map = {
            tt.MINUS: (float, "Operands must be numbers"),
            tt.SLASH: (float, "Operands must be numbers"),
            tt.STAR: (float, "Operands must be numbers"),
            tt.GREATER: (float, "Operands must be numbers"),
            tt.GREATER_EQUAL: (float, "Operands must be numbers"),
            tt.LESS: (float, "Operands must be numbers"),
            tt.LESS_EQUAL: (float, "Operands must be numbers"),
        }

        op_type = expr.operator.tokenType
        if op_type in type_map:
            expected_type, message = type_map[op_type]
            self.checkType(left, expected_type, expr.operator, message)
            self.checkType(right, expected_type, expr.operator, message)

            if op_type == tt.MINUS:
                return left - right
            elif op_type == tt.SLASH:
                return left / right
            elif op_type == tt.STAR:
                return left * right
            elif op_type == tt.GREATER:
                return left > right
            elif op_type == tt.GREATER_EQUAL:
                return left >= right
            elif op_type == tt.LESS:
                return left < right
            elif op_type == tt.LESS_EQUAL:
                return left <= right

        elif op_type == tt.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(
                expr.operator, "Operands must be two numbers or two strings.")
        elif op_type == tt.BANG_EQUAL:
            return not self.isEqual(left, right)
        elif op_type == tt.EQUAL_EQUAL:
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
