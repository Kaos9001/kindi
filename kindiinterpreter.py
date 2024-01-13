import kindiast as ast
from collections import namedtuple
from kindierrors import *
from kindilex import reserved
import json

class Value:
    def __init__(self, value=None, vtype=None):
        self.value = value
        self.type = vtype
    def __repr__(self):
        return f"{self.value} <TYPE {self.type}>"


class KindiFunction:
    def __init__(self, args=None, block=None):
        for arg in args:
            if arg in reserved:
                raise ReservedWordInArgumentsError(arg)
        self.args = args
    def expected(self):
        return [arg.type for arg in self.args]


class UserFunction(KindiFunction):
    def __init__(self, args=None, block=None):
        self.args = args
        self.block = block

class WrappedFunction(KindiFunction):
    def __init__(self, args=None, func=None):
        self.args = args
        self.func = func

    def call(self, args):
        return self.func(*args)

class OverloadedFunction(WrappedFunction):
    def __init__(self, arg_sets=None, func=None):
        self.arg_sets = arg_sets
        self.func = func
    def expected(self):
        return [[arg.type for arg in args] for args in self.arg_sets]


def evaluate(state, action):
    # Literal (ex: 2)
    if isinstance(action, ast.Block):
        block = action
        new_state, return_val = evaluate(state, block.command)
        if return_val is not None:
            return new_state, return_val
        if block.next_block is not None:
            return evaluate(new_state, block.next_block)
        else:
            return new_state, 0

    elif isinstance(action, ast.Literal):
        literal = action
        return state, Value(value=literal.value, vtype=literal.type)

    # Tentativa de acessar valor de variavel (ex: a)
    elif isinstance(action, str):
        var_name = action
        if var_name not in state:
            raise VariableNotDefinedError(var_name)
        return state, state[var_name]

    # Cadeia de comandos (ponto de entrada)

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
            elif action.optype == "%":
                return state, Value(value=left.value % right.value, vtype=left.type)
            elif action.optype == "<":
                return state, Value(value=left.value < right.value, vtype='bool')
            elif action.optype == ">":
                return state, Value(value=left.value > right.value, vtype='bool')
            elif action.optype == "<=":
                return state, Value(value=left.value <= right.value, vtype='bool')
            elif action.optype == ">=":
                return state, Value(value=left.value >= right.value, vtype='bool')
            elif action.optype == "==":
                return state, Value(value=left.value == right.value, vtype='bool')
            elif action.optype == "!=":
                return state, Value(value=left.value != right.value, vtype='bool')
        elif left.type == 'bool':
            if action.optype == "or":
                return state, Value(value=left.value or right.value, vtype=left.type)
            if action.optype == "and":
                return state, Value(value=left.value and right.value, vtype=left.type)

    elif isinstance(action, ast.Conditional):
        conditional = action
        out = None
        if evaluate(state, conditional.condition)[1].value is True:
            out = evaluate(state.copy(), conditional.on_true)[1]
        elif conditional.on_else is not None:
            out = evaluate(state.copy(), conditional.on_else)[1]
        return state, out

    elif isinstance(action, ast.Print):
        print_command = action
        candidate_value = evaluate(state, print_command.content)[1]
        if candidate_value.type != 'string' and candidate_value.type != 'subst':
            raise InvalidTypeForPrintError(candidate_value.type)
        print(candidate_value.value)
        return state, None

    elif isinstance(action, ast.Concat):
        concat = action
        left, right = evaluate(state, concat.left)[1], evaluate(state, concat.right)[1]
        if left.type != 'string' or right.type != 'string':
            raise InvalidTypesForConcatError(left.type, right.type)
        return state, Value(left.value + right.value, vtype='string')

    elif isinstance(action, ast.FunctionCall):
        call = action
        if call.id not in state:
            raise UndefinedIsNotAFunctionError(call.id)
        elif state[call.id].type != 'builtin_func' and state[call.id].type != 'user_func':
            raise NotAFunctionError(call.id)
        func = state[call.id].value
        args = [evaluate(state, candidate_arg)[1] for candidate_arg in call.args]
        if not isinstance(func, OverloadedFunction):
            arg_sets = [func.args]
        else:
            arg_sets = func.arg_sets
        if len(arg_sets) == 1 and len(args) != len(arg_sets[0]):
            raise IncorrectNumberOfArgumentsError(len(args), len(func.args))
        for arg_set in arg_sets:
            if len(args) != len(arg_set):
                continue
            for i, arg in enumerate(args):
                if arg.type != arg_set[i].type:
                    continue
            break
        else:
            raise InvalidArgumentsError(func.expected(), [arg.type for arg in call.args])
        func_state = state.copy()
        if isinstance(func, UserFunction):
            for i, arg in enumerate(args):
                func_state[func.args[i].id] = Value(value=arg.value, vtype=arg.type)
        if state[call.id].type == 'builtin_func':
            return state, func.call(args)
        else:
            out = evaluate(func_state, func.block)[1]
            return state, out

    elif isinstance(action, ast.FunctionDef):
        function_def = action
        if function_def.id in state:
            raise VariableAlreadyDefinedError(function_def.id)
        new_function = UserFunction(args=function_def.args, block=function_def.on_call)
        state[function_def.id] = Value(value=new_function, vtype='user_func')
        return state, None

    elif isinstance(action, ast.Return):
        new_state, out = evaluate(state, action.value)
        return new_state, out

