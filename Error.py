class CompilationError(Exception):
    pass

class LexicalError(CompilationError):
    pass

class SyntaxError(CompilationError):
    pass

class SemanticError(CompilationError):
    pass

class CodeGenerationError(CompilationError):
    pass

def handle_error(error_type, message):
    raise error_type(message)
