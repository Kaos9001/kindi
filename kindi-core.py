import ply.lex as lex
import ply.yacc as yacc
import importlib
import sys
import kindigrm

kindilex = importlib.import_module("kindilex")

lexer = lex.lex(module=kindilex)
parser = yacc.yacc(module=kindigrm)

with open(sys.argv[1], 'r') as file:
    content = file.read()

lexer.input(content)

# Tokenize
for tok in lexer:
    print(tok)

print(parser.parse(content, debug=True))