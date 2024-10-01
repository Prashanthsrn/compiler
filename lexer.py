import re

# Token specification
TOKENS = [
    ('NUMBER', r'\d+(\.\d*)?'),  
    ('ID', r'[A-Za-z]+'),  
    ('IF', r'\bif\b'),  
    ('ELSE', r'\belse\b'),  
    ('EQ', r'=='),  
    ('ASSIGN', r'='),  
    ('OP', r'[+\-*/]'),  
    ('LPAREN', r'\('),  
    ('RPAREN', r'\)'),  
    ('LBRACE', r'\{'),  
    ('RBRACE', r'\}'), 
    ('SEMICOLON', r';'),  
    ('WS', r'\s+'),  
]

# Lexical analyzer
def lex(characters):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_spec in TOKENS:
            pattern, regex = token_spec
            regex = re.compile(regex)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if pattern != 'WS':  # Ignore whitespace
                    tokens.append((pattern, text))
                pos = match.end(0)
                break
        if not match:
            raise RuntimeError(f"Illegal character: {characters[pos]}")
    return tokens


