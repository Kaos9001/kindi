import ply.lex as lex
import ply.yacc as yacc
# import importlib
import sys
import kindilex
import kindigrm

from pprint import pprint

# kindilex = importlib.import_module("kindilex")

lexer = lex.lex(module=kindilex)
parser = yacc.yacc(module=kindigrm)

with open(sys.argv[1], 'r') as file:
    content = file.read()

lexer.input(content)

ast = parser.parse(content)

pprint(ast.to_dict())