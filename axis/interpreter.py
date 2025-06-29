from typing import Dict, Any, List, Optional
import csv
import os

class AxisInterpreter:
    """Interpretador para a linguagem Axis"""
    
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.builtin_functions = self._setup_builtins()
    
    def _setup_builtins(self) -> Dict[str, callable]:
        """Configura funções built-in da linguagem"""
        return {
            "print": self._builtin_print,
            "read_csv": self._builtin_read_csv,
            "write_csv": self._builtin_write_csv,
            "len": self._builtin_len,
            "sum": self._builtin_sum,
            "max": self._builtin_max,
            "min": self._builtin_min
        }
    
    def _builtin_print(self, *args):
        """Função built-in para imprimir valores"""
        print(*args)
        return None
    
    def _builtin_read_csv(self, filename: str) -> List[Dict[str, Any]]:
        """Função built-in para ler arquivo CSV"""
        data = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Erro ao ler CSV: {e}")
        return data
    
    def _builtin_write_csv(self, filename: str, data: List[Dict[str, Any]], fieldnames: List[str] = None):
        """Função built-in para escrever arquivo CSV"""
        try:
            if not fieldnames and data:
                fieldnames = list(data[0].keys())
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f"Erro ao escrever CSV: {e}")
    
    def _builtin_len(self, collection) -> int:
        """Função built-in para obter tamanho de coleção"""
        if isinstance(collection, (list, dict)):
            return len(collection)
        return 0
    
    def _builtin_sum(self, collection) -> float:
        """Função built-in para somar valores"""
        if isinstance(collection, list):
            return sum(collection)
        return 0
    
    def _builtin_max(self, collection) -> Any:
        """Função built-in para encontrar valor máximo"""
        if isinstance(collection, list) and collection:
            return max(collection)
        return None
    
    def _builtin_min(self, collection) -> Any:
        """Função built-in para encontrar valor mínimo"""
        if isinstance(collection, list) and collection:
            return min(collection)
        return None
    
    def evaluate_expression(self, expr: Dict[str, Any]) -> Any:
        """Avalia uma expressão"""
        if expr["type"] == "literal":
            return expr["value"]
        
        elif expr["type"] == "identifier":
            if expr["value"] in self.variables:
                return self.variables[expr["value"]]
            else:
                raise NameError(f"Variável '{expr['value']}' não definida")
        
        elif expr["type"] == "binary_op":
            left = self.evaluate_expression(expr["left"])
            right = self.evaluate_expression(expr["right"])
            operator = expr["operator"]
            
            if operator == "+":
                return left + right
            elif operator == "-":
                return left - right
            elif operator == "*":
                return left * right
            elif operator == "/":
                return left / right
            elif operator == "%":
                return left % right
            elif operator == "==":
                return left == right
            elif operator == "!=":
                return left != right
            elif operator == "<":
                return left < right
            elif operator == ">":
                return left > right
            elif operator == "<=":
                return left <= right
            elif operator == ">=":
                return left >= right
            elif operator == "&&":
                return bool(left and right)
            elif operator == "||":
                return bool(left or right)
        
        elif expr["type"] == "unary_op":
            operand = self.evaluate_expression(expr["operand"])
            operator = expr["operator"]
            
            if operator == "-":
                return -operand
            elif operator == "!":
                return not operand
        
        elif expr["type"] == "function_call":
            func_name = expr["name"]
            arguments = [self.evaluate_expression(arg) for arg in expr["arguments"]]
            
            if func_name in self.builtin_functions:
                return self.builtin_functions[func_name](*arguments)
            elif func_name in self.functions:
                return self._call_function(func_name, arguments)
            else:
                raise NameError(f"Função '{func_name}' não definida")
        
        return None
    
    def execute_statement(self, stmt: Dict[str, Any]) -> Any:
        """Executa uma declaração"""
        if stmt["type"] == "assignment":
            value = self.evaluate_expression(stmt["expression"])
            self.variables[stmt["identifier"]] = value
            return value
        
        elif stmt["type"] == "if":
            condition = self.evaluate_expression(stmt["condition"])
            if condition:
                return self.execute_block(stmt["then_block"])
            elif stmt["else_block"]:
                return self.execute_block(stmt["else_block"])
        
        elif stmt["type"] == "for_c_style":
            self.execute_statement(stmt["init"])
            while self.evaluate_expression(stmt["condition"]):
                self.execute_block(stmt["block"])
                self.execute_statement(stmt["increment"])
        
        elif stmt["type"] == "for_in":
            collection = self.evaluate_expression(stmt["collection"])
            if isinstance(collection, (list, dict)):
                for item in collection:
                    self.variables[stmt["variable"]] = item
                    self.execute_block(stmt["block"])
        
        elif stmt["type"] == "while":
            while self.evaluate_expression(stmt["condition"]):
                self.execute_block(stmt["block"])
        
        elif stmt["type"] == "function":
            self.functions[stmt["name"]] = stmt
            return None
        
        elif stmt["type"] == "return":
            if stmt["value"]:
                return self.evaluate_expression(stmt["value"])
            return None
        
        elif stmt["type"] == "expression":
            return self.evaluate_expression(stmt["expression"])
        
        elif stmt["type"] == "block":
            return self.execute_block(stmt)
        
        return None
    
    def execute_block(self, block: Dict[str, Any]) -> Any:
        """Executa um bloco de código"""
        result = None
        for stmt in block["statements"]:
            result = self.execute_statement(stmt)
        return result
    
    def _call_function(self, func_name: str, arguments: List[Any]) -> Any:
        """Chama uma função definida pelo usuário"""
        func_def = self.functions[func_name]
        
        # Salvar estado atual das variáveis
        old_variables = self.variables.copy()
        
        # Definir parâmetros
        for i, param in enumerate(func_def["parameters"]):
            if i < len(arguments):
                self.variables[param["name"]] = arguments[i]
        
        # Executar corpo da função
        result = self.execute_block(func_def["body"])
        
        # Restaurar variáveis
        self.variables = old_variables
        
        return result
    
    def execute(self, ast: Dict[str, Any]) -> Any:
        """Executa um programa Axis"""
        if ast["type"] == "program":
            result = None
            for stmt in ast["statements"]:
                result = self.execute_statement(stmt)
            return result
        else:
            return self.execute_statement(ast)
    
    def execute_file(self, file_path: str) -> Any:
        """Executa um arquivo Axis"""
        from .parser import AxisParser
        
        parser = AxisParser()
        ast = parser.parse_file(file_path)
        return self.execute(ast)

if __name__ == "__main__":
    # Teste do interpretador
    interpreter = AxisInterpreter()
    
    test_code = """
    fun calcularTotal(preco: Float, quantidade: Int) -> Float {
        total := preco * quantidade
        return total
    }
    
    resultado := calcularTotal(10.5, 3)
    print("Total:", resultado)
    """
    
    try:
        from .parser import AxisParser
        parser = AxisParser()
        ast = parser.parse(test_code)
        interpreter.execute(ast)
    except Exception as e:
        print(f"Erro: {e}") 