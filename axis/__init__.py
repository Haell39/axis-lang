"""
Axis Language - Uma linguagem de programação inspirada em Python, Kotlin e Go

Este módulo contém a implementação completa da linguagem Axis:
- Parser para análise sintática
- Interpreter para execução de código
- Gramática definida em Lark
"""

from .parser import AxisParser
from .interpreter import AxisInterpreter

__version__ = "0.1.0"
__author__ = "Axis Language Team"

def run_file(file_path: str):
    """Executa um arquivo Axis"""
    interpreter = AxisInterpreter()
    return interpreter.execute_file(file_path)

def run_code(code: str):
    """Executa código Axis diretamente"""
    parser = AxisParser()
    interpreter = AxisInterpreter()
    ast = parser.parse(code)
    return interpreter.execute(ast)

__all__ = ['AxisParser', 'AxisInterpreter', 'run_file', 'run_code'] 