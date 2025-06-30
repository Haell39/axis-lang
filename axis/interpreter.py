from lark import Visitor
import pandas as pd
import matplotlib.pyplot as plt

class AxisInterpreter(Visitor):
    def __init__(self):
        self.env = {}

    def run(self, tree):
        self.visit(tree)

    def assign(self, tree):
        var_name = tree.children[0].value
        expr = tree.children[1]
        self.env[var_name] = self.eval_expr(expr)

    def eval_expr(self, expr):
        if expr is None or not hasattr(expr, "data"):
            return None

        if expr.data == "value":
            val = expr.children[0]
            return eval(val.value)

        elif expr.data == "string":
            return expr.children[0].value.strip('"')

        elif expr.data == "number":
            return float(expr.children[0].value)

        elif expr.data == "expr":
            if len(expr.children) == 1:
                name = expr.children[0].value
                return self.env.get(name)

        elif expr.data == "func_call":
            func_name = expr.children[0].value
            args = [self.eval_expr(arg) for arg in expr.children[1:] if arg is not None]
            if func_name == "read_csv":
                return pd.read_csv(*args)

        elif expr.data == "method_call":
            var = expr.children[0].value
            method = expr.children[1].value
            args = [self.eval_expr(arg) for arg in expr.children[2:] if arg is not None]
            return getattr(self.env[var], method)(*args)

        elif expr.data == "attr_access":
            var = expr.children[0].value
            attr = expr.children[1].value
            return getattr(self.env[var], attr)

        elif expr.data == "index":
            base = self.eval_expr(expr.children[0])
            idx = self.eval_expr(expr.children[1])
            return base[int(idx)]

    def plot_stmt(self, tree):
        var = tree.children[0].value
        col = tree.children[1].value
        df = self.env[var]
        df[col].plot()
        plt.show()

    def print_stmt(self, tree):
        text = tree.children[0].value.strip('"')
        value = self.eval_expr(tree.children[1])
        print(f"{text} {value}")
