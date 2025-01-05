from app.RuntimeError import RuntimeError


class Environment:

    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def assign(self, name, value):
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def get(self, name):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
