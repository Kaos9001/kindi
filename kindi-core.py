import ply.lex as lex
import ply.yacc as yacc
import sys
import kindilex
import kindigrm
from kindiinterpreter import evaluate, WrappedFunction, OverloadedFunction, Value, Array

from pprint import pprint

debug = False

lexer = lex.lex(module=kindilex)
parser = yacc.yacc(module=kindigrm)

with open(sys.argv[1], 'r') as file:
    content = file.read()

lexer.input(content)

ast = parser.parse(content, debug=debug)

pprint(ast.to_dict())

import json
json_out = json.dumps(ast.to_dict())
print(json_out)

kd_toString = Value(value=OverloadedFunction(
                        arg_sets=[[Value(value="s", vtype="int")],
                                  [Value(value="s", vtype="float")],
                                  [Value(value="s", vtype="bool")],
                                  [Value(value="s", vtype="array")]],
                        func=lambda s: Value(value=str(s.value), vtype="string")),
                    vtype='builtin_func')

kd_fill = Value(value=OverloadedFunction(
                        arg_sets=[[Value(value="val", vtype="int"), Value(value="n", vtype="int")],
                                  [Value(value="val", vtype="float"), Value(value="n", vtype="int")],
                                  [Value(value="val", vtype="bool"), Value(value="n", vtype="int")]],
                        func=lambda val, n: Value(value=Array(
                            vtype=val.type,
                            length=n.value,
                            items=[Value(value=val.value, vtype=val.type) for _ in range(n.value)],
                        ), vtype="array")),
                    vtype='builtin_func')


kd_rot = Value(vtype="builtin_func", value=WrappedFunction(
    args=[Value(value="to_rotate", vtype="subst"), Value(value="n", vtype='int')],
    func=lambda s, n: Value(value=s.value[n.value:] + s.value[:n.value], vtype='subst')))

kd_ind = Value(vtype="builtin_func", value=WrappedFunction(
    args=[Value(value="char", vtype="string")],
    func=lambda s: Value(value="abcdefghijklmnopqrstuvwxyz".index(s.value.lower()), vtype='int')))

def ind(char):
    if len(char) != 1:
        raise Exception()



init_state = {
    "toString":kd_toString,
    "rot":kd_rot,
    "fill":kd_fill,
    "ALPH": Value(value="abcdefghijklmnopqrstuvwxyz", vtype="string"),
    "ALPHSUB": Value(value="abcdefghijklmnopqrstuvwxyz", vtype="subst"),
    }
print(f"KINDI: RUNNING {sys.argv[1]}")
final_state = evaluate(init_state, ast)
print()
print(f"Final Memory State: {final_state}")
