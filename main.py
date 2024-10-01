from lexer import Lexer
from Parser import Parser
from SemanticAnalyzer import SemanticAnalyzer
from IRGenerator import IRGenerator
from CodeGen import CodeGen
from Error import Error

def main():
    try:
        with open('input.txt', 'r') as file:
            text = file.read()

        lexer = Lexer(text)
        parser = Parser(lexer)
        ast = parser.parse()

        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)

        ir_generator = IRGenerator()
        ir = ir_generator.generate(ast)

        code_gen = CodeGen(ir)
        python_code = code_gen.generate()

        print("Generated Python code:")
        print(python_code)

    except Error as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()