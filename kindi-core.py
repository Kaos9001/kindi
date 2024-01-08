import ply.lex as lex
import importlib
kindilex = importlib.import_module("kindi-lex")


lexer = lex.lex(module=kindilex)
lexer.input()
