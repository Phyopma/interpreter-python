from app.RuntimeError import RuntimeError


class Environment:

    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values.keys():
            return self.values[name]

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
