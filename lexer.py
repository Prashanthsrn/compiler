import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0 
        self.keywords = {'if', 'else', 'int', 'float'}  
    
    def tokenize(self):
        patterns = [
            ('KEYWORD', r'\b(if|else|int|float)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('NUMBER', r'\b\d+\b'),
            ('OPERATOR', r'[+\-*/=]'),
            ('COMPARISON', r'(==|!=|<=|>=|<|>)'),  
            ('SEMICOLON', r';'),
            ('OPEN_PAREN', r'\('),
            ('CLOSE_PAREN', r'\)'),
            ('OPEN_BRACE', r'\{'),
            ('CLOSE_BRACE', r'\}'),
            ('WHITESPACE', r'\s+')
        ]

        # Process the code by matching patterns using regex
        while self.pos < len(self.code):
            match = None
            for token_type, pattern in patterns:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)
                if match:
                    token_value = match.group(0)
                    if token_type != 'WHITESPACE':  
                        self.tokens.append((token_type, token_value))
                    self.pos = match.end(0)
                    break
            if not match:
                raise SyntaxError(f"Illegal character at position {self.pos}: {self.code[self.pos]}")
        return self.tokens
