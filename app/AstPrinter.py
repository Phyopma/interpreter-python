from app.tool.Expr import Visitor, Expr
from app.TokensType import TokensType as tt
from app.Token import Token


class AstPrinter(Visitor):
    def print(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value).lower()

    def visit_logical_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_call_expr(self, expr):
        return self.parenthesize("call", expr.callee, expr.paren, expr.arguments)

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def visit_assign_expr(self, expr):
        return super().visit_assign_expr(expr)

    def parenthesize(self, name, *exprs):
        builder = []
        builder.append("(")
        builder.append(name)
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))
        builder.append(")")
        return "".join(builder)

    def main():
        expression = Expr.Binary(
            Expr.Unary(
                Token(tt.MINUS, "-", None, 1),
                Expr.Literal(123)
            ),
            Token(tt.STAR, "*", None, 1),
            Expr.Grouping(
                Expr.Literal(45.67)
            )
        )
        print(AstPrinter().print(expression))


if __name__ == "__main__":
    AstPrinter.main()
