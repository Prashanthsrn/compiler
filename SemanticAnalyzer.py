class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}

    def analyze(self):
        for statement in self.ast:
            if statement[0] == "ASSIGNMENT":
                _, var_name, value = statement
                if var_name[1] in self.symbol_table:
                    raise Exception(f"Variable {var_name[1]} already declared")
                self.symbol_table[var_name[1]] = value[1]
            elif statement[0] == "IF_ELSE":
                self.analyze_if_else(statement)

    def analyze_if_else(self, statement):
        _, condition, if_block, else_block = statement
        # Ensure the condition uses declared variables
        if condition[1] not in self.symbol_table:
            raise Exception(f"Variable {condition[1]} in condition not declared")

        # Analyze statements inside the if block
        for stmt in if_block:
            self.analyze_statement(stmt)

        # Analyze statements inside the else block (if present)
        if else_block:
            for stmt in else_block:
                self.analyze_statement(stmt)

    def analyze_statement(self, statement):
        if statement[0] == "ASSIGNMENT":
            _, var_name, value = statement
            self.symbol_table[var_name[1]] = value[1]
