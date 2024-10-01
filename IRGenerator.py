class IRGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.new_temp()
        op = node.op.type.lower()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp

    def visit_UnaryOp(self, node):
        expr = self.visit(node.expr)
        temp = self.new_temp()
        op = node.op.type.lower()
        self.emit(f"{temp} = {op}{expr}")
        return temp

    def visit_Num(self, node):
        return str(node.value)

    def visit_Var(self, node):
        return node.value

    def visit_Assign(self, node):
        var_name = node.left.value
        right = self.visit(node.right)
        self.emit(f"{var_name} = {right}")

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_IfElse(self, node):
        condition = self.visit(node.condition)
        label_else = self.new_label()
        label_end = self.new_label()

        self.emit(f"if not {condition} goto {label_else}")
        self.visit(node.if_body)
        self.emit(f"goto {label_end}")
        self.emit(f"{label_else}:")
        if node.else_body:
            self.visit(node.else_body)
        self.emit(f"{label_end}:")

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self):
        self.temp_counter += 1
        return f"L{self.temp_counter}"

    def emit(self, instruction):
        self.instructions.append(instruction)

    def generate(self, node):
        self.visit(node)
        return self.instructions