from app.Callable import Callable
from app.Environment import Environment
from app.Return import Return


class Function(Callable):
    def __init__(self, declaration, closure, isInitializer=False):
        self.declaration = declaration
        self.closure = closure
        self.isIntializer = isInitializer

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as returnValue:
            return returnValue.value
        if self.isIntializer:
            return self.closure.getAt(0, "this")
        return None

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return Function(self.declaration, environment, self.isIntializer)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
