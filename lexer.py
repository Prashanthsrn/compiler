import re

class Lexer:
    # List of token types with their corresponding regex patterns
    TOKENS = [
        ("TYPE", r'\bint\b|\bfloat\b'),  
        ("NUMBER", r'\b\d+\b'),          
        ("IDENTIFIER", r'[a-zA-Z_]\w*'), 
        ("OPERATOR", r'[\+\-\*/]'),      
        ("ASSIGNMENT", r'='),            
        ("IF", r'\bif\b'),               
        ("ELSE", r'\belse\b'),           
        ("COMPARISON", r'[><=!]'),       
        ("BRACKET_OPEN", r'\{'),         
        ("BRACKET_CLOSE", r'\}'),        
        ("WHITESPACE", r'[ \t]+'),       
        ("NEWLINE", r'\n'),              
        ("UNKNOWN", r'.'),               
    ]

    def __init__(self, code):
        self.code = code  
        self.pos = 0      
        self.tokens = []

    # Main function to tokenize the input code
    def tokenize(self):
        while self.pos < len(self.code): 
            match = None
            for token_type, pattern in self.TOKENS:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)
                if match:
                    if token_type != "WHITESPACE":  
                        self.tokens.append((token_type, match.group(0)))  
                    self.pos = match.end(0)  
                    break
            if not match:
                raise Exception(f"Unexpected character at position {self.pos}")
        return self.tokens  
