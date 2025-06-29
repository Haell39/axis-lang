import sys
from axis.parser import AxisParser
from axis.interpreter import AxisInterpreter

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "run":
        print("Uso: python main.py run <arquivo.axis>")
        sys.exit(1)

    filename = sys.argv[2]

    with open(filename, "r") as f:
        code = f.read()

    tree = AxisParser().parse(code)
    AxisInterpreter().run(tree)
