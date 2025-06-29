#!/usr/bin/env python3
"""
Script principal para executar arquivos da linguagem Axis
"""

import sys
import os
from axis import run_file, run_code

def main():
    if len(sys.argv) < 2:
        print("Uso: python run_axis.py <arquivo.axis>")
        print("   ou: python run_axis.py -c '<código>'")
        sys.exit(1)
    
    if sys.argv[1] == "-c" and len(sys.argv) >= 3:
        # Executar código diretamente
        code = sys.argv[2]
        try:
            result = run_code(code)
            if result is not None:
                print("Resultado:", result)
        except Exception as e:
            print(f"Erro: {e}")
            sys.exit(1)
    
    else:
        # Executar arquivo
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Erro: Arquivo '{file_path}' não encontrado")
            sys.exit(1)
        
        try:
            result = run_file(file_path)
            if result is not None:
                print("Resultado:", result)
        except Exception as e:
            print(f"Erro: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main() 