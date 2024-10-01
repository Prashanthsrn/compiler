from Error import Error

class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, symbol):
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        return self.symbols.get(name)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Error(f"No visit_{type(node).__name__} method")

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Num(self, node):
        pass

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:
            raise Error(f"Variable '{var_name}' is not defined")

    def visit_Assign(self, node):
        var_name = node.left.value
        self.visit(node.right)
        var_symbol = Symbol(var_name)
        self.symbol_table.define(var_symbol)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_IfElse(self, node):
        self.visit(node.condition)
        self.visit(node.if_body)
        if node.else_body:
            self.visit(node.else_body)

    def analyze(self, node):
        self.visit(node)