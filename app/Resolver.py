import app.tool.Expr as Expr
import app.tool.Stmt as Stmt
import app.error as error
from app.FunctionsType import FunctionsType as ft
from app.ClassType import ClassType as ct


class Resolver(Expr.Visitor, Stmt.Visitor):
    interpreter = None
    # stack of dictionaries
    scopes = []
    current_function = ft.NONE
    current_class = ct.NONE

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None

    def visit_class_stmt(self, stmt):
        enclosing_class = self.current_class
        self.current_class = ct.CLASS
        self.declare(stmt.name)
        if (stmt.superclass is not None):
            if (stmt.name.lexeme == stmt.superclass.name.lexeme):
                error.token_error(
                    stmt.superclass.name, "A class cannot inherit from itself.")
            self.current_class = ct.SUBCLASS
            self.resolve_expr(stmt.superclass)

        if (stmt.superclass is not None):
            self.begin_scope()
            self.scopes[-1]["super"] = True

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = ft.METHOD
            if method.name.lexeme == "init":
                declaration = ft.INITIALIZER
            elif method.kind == "static":
                declaration = ft.STATIC
            elif method.kind == "getter":
                declaration = ft.GETTER
            self.resolve_function(method, declaration)
        self.define(stmt.name)
        self.end_scope()

        if (stmt.superclass is not None):
            self.end_scope()
        self.current_class = enclosing_class
        return None

    def resolve(self, statements):
        for statement in statements:
            self.resolve_statement(statement)

    def resolve_statement(self, statement):
        statement.accept(self)

    def resolve_expr(self, expr):
        expr.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)
        return None

    def declare(self, name):
        if not self.scopes:
            return
        scope = self.scopes[-1]  # get the current scope
        if name.lexeme in scope:
            error.token_error(
                name, "Variable with this name already declared in this scope.")
        scope[name.lexeme] = False

    def define(self, name):
        # checking scopes is not empty
        if not self.scopes:
            return
        scope = self.scopes[-1]

        scope[name.lexeme] = True

    def visit_variable_expr(self, expr):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            error.token_error(
                expr.name, "Cannot read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)
        return None

    def resolve_local(self, expr, name):
        # iterate from the current scope to the global scope
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
        # Not found. Assume it is global.

    def visit_assign_expr(self, expr):
        # resolve the value if it is an expression e.g. a = b + c
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)
        return None

    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, ft.FUNCTION)
        return None

    def resolve_function(self, stmt, type):
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for param in stmt.params:
            self.declare(param)
            self.define(param)
        self.resolve(stmt.body)
        self.end_scope()
        self.current_function = enclosing_function

    def visit_expression_stmt(self, stmt):
        self.resolve_expr(stmt.expression)
        return None

    def visit_if_stmt(self, stmt):
        self.resolve_expr(stmt.condition)
        self.resolve_statement(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve_statement(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt):
        self.resolve_expr(stmt.expression)
        return None

    def visit_return_stmt(self, stmt):
        if self.current_function == ft.NONE:
            error.token_error(
                stmt.keyword, "Cannot return from top-level code.")
        if stmt.value is not None:
            if self.current_function == ft.INITIALIZER:
                error.token_error(
                    stmt.keyword, "Cannot return a value from an initializer.")
            self.resolve_expr(stmt.value)
        return None

    def visit_while_stmt(self, stmt):
        self.resolve_expr(stmt.condition)
        self.resolve_statement(stmt.body)
        return None

    def visit_binary_expr(self, expr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None

    def visit_call_expr(self, expr):
        self.resolve_expr(expr.callee)
        for argument in expr.arguments:
            self.resolve_expr(argument)
        return None

    def visit_get_expr(self, expr):
        self.resolve_expr(expr.object)
        return None

    def visit_grouping_expr(self, expr):
        self.resolve_expr(expr.expression)
        return None

    def visit_literal_expr(self, expr):
        return None

    def visit_logical_expr(self, expr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None

    def visit_set_expr(self, expr):
        self.resolve_expr(expr.value)
        self.resolve_expr(expr.object)
        return None

    def visit_super_expr(self, expr):
        if (self.current_class == ct.NONE):
            error.token_error(
                expr.keyword, "Cannot use 'super' outside of a class.")
        elif (self.current_class != ct.SUBCLASS):
            error.token_error(
                expr.keyword, "Cannot use 'super' in a class with no superclass.")

        self.resolve_local(expr, expr.keyword)
        return None

    def visit_this_expr(self, expr):
        if self.current_class == ct.NONE:
            error.token_error(
                expr.keyword, "Cannot use 'this' outside of a class.")
            return None
        if self.current_function == ft.STATIC:
            error.token_error(
                expr.keyword, "Cannot use 'this' in a static method.")
            return None
        self.resolve_local(expr, expr.keyword)
        return None

    def visit_unary_expr(self, expr):
        self.resolve_expr(expr.right)
        return None
