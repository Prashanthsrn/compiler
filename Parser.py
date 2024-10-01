class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0  

    def get_current_token(self):
        return self.tokens[self.current_token]

    def eat(self, token_type):
        if self.get_current_token()[0] == token_type:
            self.current_token += 1
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.get_current_token()[0]}")

    def parse(self):
        statements = []
        while self.current_token < len(self.tokens):
            token_type, token_value = self.get_current_token()

            if token_type == 'KEYWORD' and token_value == 'if':
                statements.append(self.parse_if_else())
            elif token_type == 'KEYWORD':
                statements.append(self.parse_declaration())
            else:
                statements.append(self.parse_expression())
        return statements

    def parse_if_else(self):
        self.eat('KEYWORD')  
        self.eat('OPEN_PAREN')  
        condition = self.parse_expression()  
        self.eat('CLOSE_PAREN')  
        self.eat('OPEN_BRACE')  
        if_block = self.parse_block()  
        self.eat('CLOSE_BRACE')  

        else_block = None
        if self.get_current_token()[1] == 'else':  
            self.eat('KEYWORD')  
            self.eat('OPEN_BRACE') 
            else_block = self.parse_block()  
            self.eat('CLOSE_BRACE') 

        return ('IF_ELSE', condition, if_block, else_block)

    def parse_block(self):
        statements = []
        while self.get_current_token()[0] != 'CLOSE_BRACE':
            statements.append(self.parse_expression())
        return statements

    def parse_expression(self):
        token_type, token_value = self.get_current_token()

        if token_type == 'IDENTIFIER':  
            var_name = self.get_current_token()
            self.eat('IDENTIFIER')
            self.eat('OPERATOR')  
            value = self.get_current_token()
            self.eat('NUMBER')
            self.eat('SEMICOLON')
            return ('ASSIGNMENT', var_name, value)

        if token_type == 'NUMBER' or token_type == 'IDENTIFIER':  
            left = self.get_current_token()
            self.eat(token_type)
            op = self.get_current_token()  
            self.eat('COMPARISON')
            right = self.get_current_token()
            self.eat('NUMBER')
            return ('BINARY_OP', left, op, right)

        raise SyntaxError("Unknown expression")
