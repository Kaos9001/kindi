import ply.lex as lex
import importlib
import sys

kindilex = importlib.import_module("kindilex")

lexer = lex.lex(module=kindilex)

with open(sys.argv[1], 'r') as file:
    content = file.read()

lexer.input(content)

# Tokenize
for tok in lexer:
    print(tok)