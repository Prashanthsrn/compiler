class CodeGenerator:
    def __init__(self, ir_code):
        self.ir_code = ir_code
        self.target_code = []

    def generate_code(self):
        for ir in self.ir_code:
            if ir.startswith('IF_FALSE'):
                self.handle_if_false(ir)
            elif ir.startswith('GOTO'):
                self.target_code.append(f'{ir}')
            elif ir.endswith(':'):
                self.target_code.append(f'{ir}')
            else:
                self.target_code.append(self.handle_assignment(ir))

        return self.target_code

    def handle_if_false(self, ir):
        parts = ir.split(' ')
        condition_var = parts[1]
        operator = parts[2]
        comparison_value = parts[3]
        goto_label = parts[-1]

        # Translate to target language
        self.target_code.append(f'IF {condition_var} {operator} {comparison_value} GOTO {goto_label}')

    # Assignment stays the same, e.g., x = 20
    def handle_assignment(self, ir):
        return ir  

    def write_to_file(self, filename='output.asm'):
        with open(filename, 'w') as f:
            for line in self.target_code:
                f.write(line + '\n')
