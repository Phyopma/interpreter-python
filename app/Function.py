from app.Callable import Callable
from app.Environment import Environment


class Function(Callable):
    def __init__(self, declaration):
        self.declaration = declaration

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        interpreter.execute_block(self.declaration.body, environment)
        return None

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
