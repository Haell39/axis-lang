from lark import Lark, Transformer, v_args
from typing import List, Dict, Any, Optional
import os

class AxisTransformer(Transformer):
    """Transformador para converter a árvore sintática em estruturas de dados Python"""
    
    def start(self, statements):
        return {"type": "program", "statements": statements}
    
    def statement(self, args):
        return args[0]
    
    def assignment(self, args):
        # args: [IDENTIFIER, expression]
        if len(args) >= 2:
            identifier, expression = args[0], args[1]
            return {
                "type": "assignment",
                "identifier": str(identifier),
                "expression": expression
            }
        else:
            raise ValueError(f"assignment: argumentos inesperados: {args}")
    
    def if_statement(self, args):
        # args: [expression, block] ou [expression, block, block]
        condition = args[0]
        then_block = args[1]
        else_block = args[2] if len(args) > 2 else None
        return {
            "type": "if",
            "condition": condition,
            "then_block": then_block,
            "else_block": else_block
        }
    
    def for_statement(self, args):
        # C-style: [assignment, expression, assignment, block]
        # For-in: [IDENTIFIER, expression, block]
        if len(args) == 4:
            return {
                "type": "for_c_style",
                "init": args[0],
                "condition": args[1],
                "increment": args[2],
                "block": args[3]
            }
        elif len(args) == 3:
            return {
                "type": "for_in",
                "variable": str(args[0]),
                "collection": args[1],
                "block": args[2]
            }
        else:
            raise ValueError(f"for_statement: argumentos inesperados: {args}")
    
    def while_statement(self, args):
        return {
            "type": "while",
            "condition": args[1],
            "block": args[2]
        }
    
    def function_declaration(self, args):
        # args: [IDENTIFIER, parameters?, type?, block]
        name = str(args[0])
        parameters = args[1] if len(args) > 2 else []
        return_type = args[2] if len(args) > 3 else None
        body = args[-1]
        return {
            "type": "function",
            "name": name,
            "parameters": parameters,
            "return_type": return_type,
            "body": body
        }
    
    def parameters(self, args):
        return args
    
    def parameter(self, args):
        return {
            "name": str(args[0]),
            "type": str(args[1])
        }
    
    def return_statement(self, args):
        return {
            "type": "return",
            "value": args[0] if args else None
        }
    
    def expression_statement(self, args):
        return {
            "type": "expression",
            "expression": args[0]
        }
    
    def block(self, args):
        return {
            "type": "block",
            "statements": args
        }
    
    def expression(self, args):
        return args[0]
    
    def logical_or(self, args):
        if len(args) == 1:
            return args[0]
        return {
            "type": "binary_op",
            "operator": "||",
            "left": args[0],
            "right": args[2]
        }
    
    def logical_and(self, args):
        if len(args) == 1:
            return args[0]
        return {
            "type": "binary_op",
            "operator": "&&",
            "left": args[0],
            "right": args[2]
        }
    
    def equality(self, args):
        if len(args) == 1:
            return args[0]
        return {
            "type": "binary_op",
            "operator": str(args[1]),
            "left": args[0],
            "right": args[2]
        }
    
    def comparison(self, args):
        if len(args) == 1:
            return args[0]
        return {
            "type": "binary_op",
            "operator": str(args[1]),
            "left": args[0],
            "right": args[2]
        }
    
    def term(self, args):
        if len(args) == 1:
            return args[0]
        return {
            "type": "binary_op",
            "operator": str(args[1]),
            "left": args[0],
            "right": args[2]
        }
    
    def factor(self, args):
        if len(args) == 1:
            return args[0]
        return {
            "type": "binary_op",
            "operator": str(args[1]),
            "left": args[0],
            "right": args[2]
        }
    
    def unary(self, args):
        if len(args) == 1:
            return args[0]
        return {
            "type": "unary_op",
            "operator": str(args[0]),
            "operand": args[1]
        }
    
    def primary(self, args):
        return args[0]
    
    def function_call(self, args):
        return {
            "type": "function_call",
            "name": str(args[0]),
            "arguments": args[1] if len(args) > 1 else []
        }
    
    def arguments(self, args):
        return args
    
    def IDENTIFIER(self, token):
        return {"type": "identifier", "value": str(token)}
    
    def NUMBER(self, token):
        value = float(token) if '.' in token else int(token)
        return {"type": "literal", "value": value, "data_type": "number"}
    
    def STRING(self, token):
        return {"type": "literal", "value": token[1:-1], "data_type": "string"}
    
    def type(self, args):
        return str(args[0])

class AxisParser:
    """Parser para a linguagem Axis"""
    
    def __init__(self):
        grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.lark')
        with open(grammar_path, 'r', encoding='utf-8') as f:
            grammar = f.read()
        
        self.parser = Lark(grammar, parser='lalr', transformer=AxisTransformer())
    
    def parse(self, code: str) -> Dict[str, Any]:
        """Parse o código Axis e retorna a árvore sintática"""
        try:
            tree = self.parser.parse(code)
            return tree
        except Exception as e:
            raise SyntaxError(f"Erro de sintaxe: {e}")
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse um arquivo Axis"""
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        return self.parse(code)

if __name__ == "__main__":
    # Teste do parser
    parser = AxisParser()
    
    test_code = """
    fun calcularTotal(preco: Float, quantidade: Int) -> Float {
        total := preco * quantidade
        return total
    }
    
    if (total > 100) {
        desconto := total * 0.1
    }
    """
    
    try:
        result = parser.parse(test_code)
        print("Parse bem-sucedido!")
        print(result)
    except Exception as e:
        print(f"Erro: {e}") 