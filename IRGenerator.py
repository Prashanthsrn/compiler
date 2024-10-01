class IRGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.ir_code = []
        self.label_count = 0

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate_ir(self):
        for statement in self.ast:
            if statement[0] == "IF_ELSE":
                self.generate_if_else(statement)
            elif statement[0] == "ASSIGNMENT":
                self.generate_assignment(statement)
        return self.ir_code

    def generate_if_else(self, statement):
        _, condition, if_block, else_block = statement
        false_label = self.new_label()
        end_label = self.new_label()

        # IR for condition check and jump if false
        self.ir_code.append(f"IF_FALSE {condition[1][1]} {condition[2][1]} GOTO {false_label}")

        # IR for the if block
        for stmt in if_block:
            self.generate_assignment(stmt)

        # Jump to the end after executing the if block
        self.ir_code.append(f"GOTO {end_label}")

        # Else block, if present
        self.ir_code.append(f"{false_label}:")
        if else_block:
            for stmt in else_block:
                self.generate_assignment(stmt)

        # End of if-else statement
        self.ir_code.append(f"{end_label}:")

    def generate_assignment(self, statement):
        _, var_name, value = statement
        # IR for assignment
        self.ir_code.append(f"{var_name[1]} = {value[1]}")

