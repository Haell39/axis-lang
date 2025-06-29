from lark import Lark

with open("axis/grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr")

class AxisParser:
    def parse(self, code):
        return parser.parse(code)
