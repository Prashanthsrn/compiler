from Error import Error

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Compound(AST):
    def __init__(self):
        self.children = []

class IfElse(AST):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Error(message)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, but got {self.current_token.type}")

    def program(self):
        node = self.compound_statement()
        return node

    def compound_statement(self):
        nodes = self.statement_list()
        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type != 'EOF' and self.current_token.type != 'RBRACE':
            results.append(self.statement())
        return results

    def statement(self):
        if self.current_token.type == 'ID':
            node = self.assignment_statement()
        elif self.current_token.type == 'IF':
            node = self.if_statement()
        else:
            node = self.expr()
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat('ASSIGN')
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def if_statement(self):
        self.eat('IF')
        condition = self.expr()
        self.eat('LBRACE')
        if_body = self.compound_statement()
        self.eat('RBRACE')
        
        if self.current_token.type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            else_body = self.compound_statement()
            self.eat('RBRACE')
        else:
            else_body = None
        
        return IfElse(condition, if_body, else_body)

    def variable(self):
        node = Var(self.current_token)
        self.eat('ID')
        return node

    def expr(self):
        node = self.arithmetic_expr()
        if self.current_token.type in ('LT', 'GT', 'LTE', 'GTE', 'EQUALS'):
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(left=node, op=token, right=self.arithmetic_expr())
        return node

    def arithmetic_expr(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
            elif token.type == 'MINUS':
                self.eat('MINUS')
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            token = self.current_token
            if token.type == 'MULTIPLY':
                self.eat('MULTIPLY')
            elif token.type == 'DIVIDE':
                self.eat('DIVIDE')
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == 'PLUS':
            self.eat('PLUS')
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == 'MINUS':
            self.eat('MINUS')
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == 'INTEGER':
            self.eat('INTEGER')
            return Num(token)
        elif token.type == 'FLOAT':
            self.eat('FLOAT')
            return Num(token)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        else:
            node = self.variable()
            return node

    def parse(self):
        return self.program()