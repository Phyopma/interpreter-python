import sys


def main():
    if (len(sys.argv) != 2):
        print("Usage: generate_ast <output_directory>", file=sys.stderr)
        exit(64)
    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", [
        "Assign   : name, value",
        "Binary   : left, operator, right",
        "Call     : callee, paren, arguments",
        "Get      : object, name",
        "Grouping : expression",
        "Literal  : value",
        "Logical  : left, operator, right",
        "Set      : object, name, value",
        "This     : keyword",
        "Unary    : operator, right",
        "Variable : name"
    ])

    define_ast(output_dir, "Stmt", [
        "Block      : statements",
        "Class      : name, methods",
        "Expression : expression",
        "Function   : name, params, body, kind",
        "If         : condition, then_branch, else_branch",
        "Print      : expression",
        "Return     : keyword, value",
        "Var        : name, initializer",
        "While      : condition, body"
    ])


def define_ast(output_dir,  base_name, types):
    path = output_dir + "/" + base_name + ".py"
    with open(path, "w") as file:
        file.write("from abc import ABC, abstractmethod")
        file.write("\nclass " + base_name + "(ABC):")
        file.write("\n    @abstractmethod")
        file.write("\n    def accept(self, visitor):")
        file.write("\n        pass")
        define_visitor(file, base_name, types)
        for type in types:
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            define_type(file, base_name, class_name, fields)


def define_visitor(file, base_name, types):
    file.write("\nclass Visitor(ABC):")
    for type in types:
        type_name = type.split(":")[0].strip()
        file.write("\n    @abstractmethod")
        file.write("\n    def visit_" + type_name.lower() + "_" +
                   base_name.lower() + "(self, " + base_name.lower() + "):")
        file.write("\n        pass")


def define_type(file, base_name, class_name, fields):
    file.write("\nclass " + class_name + "(" + base_name + "):")

    # Define constructor
    file.write("\n    def __init__(self, " + fields + "):")

    # Store parameters in fields
    fields_list = fields.split(", ")
    for field in fields_list:
        name = field.strip()
        file.write("\n        self." + name + " = " + name)

    # Implement accept method
    file.write("\n    def accept(self, visitor):")
    file.write("\n        return visitor.visit_" +
               class_name.lower() + "_" + base_name.lower() + "(self)")


if __name__ == "__main__":
    main()
