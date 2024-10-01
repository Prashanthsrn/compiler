class CodeGen:
    def __init__(self, ir):
        self.ir = ir
        self.code = []
        self.indentation = 0
        self.op_map = {
            'plus': '+',
            'minus': '-',
            'multiply': '*',
            'divide': '/',
            'lt': '<',
            'gt': '>',
            'lte': '<=',
            'gte': '>=',
            'equals': '=='
        }

    def generate(self):
        for instruction in self.ir:
            parts = instruction.split()
            if '=' in instruction:
                self.handle_assignment(parts)
            elif instruction.startswith('if'):
                self.handle_if(parts)
            elif instruction.startswith('goto'):
                self.handle_goto(parts)
            elif instruction.endswith(':'):
                self.handle_label(instruction)
            else:
                self.code.append(self.indent() + instruction)

        return '\n'.join(self.code)

    def handle_assignment(self, parts):
        target = parts[0]
        if len(parts) > 3:  # Binary operation
            left = parts[2]
            op = self.op_map.get(parts[3], parts[3])
            right = parts[4]
            self.code.append(self.indent() + f"{target} = {left} {op} {right}")
        else:  # Simple assignment
            value = ' '.join(parts[2:])
            self.code.append(self.indent() + f"{target} = {value}")

    def handle_if(self, parts):
        condition = ' '.join(parts[2:-2])
        # Replace operators in condition
        for op_name, op_symbol in self.op_map.items():
            condition = condition.replace(op_name, op_symbol)
        label = parts[-1]
        self.code.append(self.indent() + f"if not ({condition}):")
        self.indentation += 1
        self.code.append(self.indent() + f"    goto {label}")
        self.indentation -= 1

    def handle_goto(self, parts):
        label = parts[1]
        self.code.append(self.indent() + f"# goto {label}")

    def handle_label(self, instruction):
        self.code.append(f"# {instruction}")

    def indent(self):
        return "    " * self.indentation