from app.Callable import Callable
from app.Instance import Instance


class Class(Instance, Callable):
    def __init__(self, name, methods, static_methods):
        super().__init__(self)
        self.methods = methods
        self.static_methods = static_methods
        self.name = name

    def __str__(self):
        return self.name

    def arity(self):
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def call(self, interpreter, arguments):
        instance = Instance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        if name in self.static_methods:
            return self.static_methods[name]
        return None
