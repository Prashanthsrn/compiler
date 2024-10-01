class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def eat(self, token_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token_type} at {self.pos}")

    def factor(self):
        token = self.tokens[self.pos]
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ('number', token[1])
        elif token[0] == 'ID':
            self.eat('ID')
            return ('id', token[1])
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expression()
            self.eat('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OP':
            op = self.tokens[self.pos]
            self.eat('OP')
            node = ('binop', node, op[1], self.factor())
        return node

    def expression(self):
        return self.term()

    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
        if_true = self.expression()
        self.eat('RBRACE')
        self.eat('ELSE')
        self.eat('LBRACE')
        if_false = self.expression()
        self.eat('RBRACE')
        return ('if', condition, if_true, if_false)

    def parse(self):
        return self.if_statement()

# # Example input tokens
# parser = Parser(tokens)
# ast = parser.parse()
# print(ast)
