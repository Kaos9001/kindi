import kindiast as ast
from collections import namedtuple
from kindierrors import *

class Value:
    def __init__(self, value=None, vtype=None):
        self.value = value
        self.type = vtype
    def __repr__(self):
        return f"{self.value} <TYPE {self.type}>"


def evaluate(state, action):
    # Literal (ex: 2)
    if isinstance(action, ast.Literal):
        literal = action
        return state, Value(value=literal.value, vtype=literal.type)

    # Tentativa de acessar valor de variavel (ex: a)
    elif isinstance(action, str):
        var_name = action
        if var_name not in state:
            raise VariableNotDefinedError(var_name)
        return state, state[var_name]

    # Cadeia de comandos (ponto de entrada)
    elif isinstance(action, ast.Block):
        block = action
        new_state = evaluate(state, block.command)[0]
        if block.next_block is not None:
            return evaluate(new_state, block.next_block)
        else:
            return new_state, 0

    # Declaracao de variaveis (ex: int a = 1)
    elif isinstance(action, ast.Assign):
        assignment = action
        if assignment.id in state:
            raise VariableAlreadyDefinedError(assignment.id)
        candidate_value = evaluate(state, assignment.value)[1]
        if candidate_value.type != assignment.type:
            raise AssignmentUnmatchedTypeError(candidate_value.type, assignment.type)
        state[assignment.id] = Value(value=candidate_value.value, vtype=assignment.type)
        return state, None

    # Redefinicao de valor de variavel (ex: a = 2)
    elif isinstance(action, ast.Reassign):
        reassignment = action
        if reassignment.id not in state:
            raise VariableNotDefinedError(reassignment.id)
        candidate_value = evaluate(state, reassignment.value)[1]
        if candidate_value.type != state[reassignment.id].type:
            raise ReassignmentUnmatchedTypeError(candidate_value.type, state[reassignment.id].type)
        state[reassignment.id].value = candidate_value.value
        return state, None

    # Operacoes binarias (ex: a > b)
    elif isinstance(action, ast.BinOp):
        left, right = evaluate(state, action.left)[1], evaluate(state, action.right)[1]
        if left.type != right.type:
            raise SyntaxError("tipos incompatives na operacao binop")
        elif left.type == 'int' or left.type == 'float':
            if action.optype == "+":
                return state, Value(value=left.value + right.value, vtype=left.type)
            elif action.optype == "-":
                return state, Value(value=left.value - right.value, vtype=left.type)
            elif action.optype == "*":
                return state, Value(value=left.value * right.value, vtype=left.type)
            elif action.optype == "/":
                if right.value == 0:
                    raise ZeroDivisionError()
                if left.type == "float":
                    return state, Value(value=left.value / right.value, vtype=left.type)
                elif left.type == "int":
                    return state, Value(value=left.value // right.value, vtype=left.type)
                else:
                    print("????????????")
            elif action.optype == "<":
                return state, Value(value=left.value < right.value, vtype='bool')
            # TODO outros operadores
        elif left.type == 'bool':
            if action.optype == "or":
                return state, Value(value=left.value or right.value, vtype=left.type)
            if action.optype == "and":
                return state, Value(value=left.value and right.value, vtype=left.type)

    elif isinstance(action, ast.Conditional):
        conditional = action
        if evaluate(state, conditional.condition)[1].value is True:
            evaluate(state, conditional.on_true)
        elif conditional.on_else is not None:
            evaluate(state, conditional.on_else)
        return state, None

    elif isinstance(action, ast.Print):
        print_command = action
        candidate_value = evaluate(state, print_command.content)[1]
        print(candidate_value.value)
        return state, None