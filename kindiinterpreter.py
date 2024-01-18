import kindiast as ast
from collections import Counter
from kindierrors import *
from kindilex import reserved
from pathlib import Path
from cipher import call_encrypt_function


def is_valid_subst(subst):
    return len(subst) == 26 and Counter(subst.lower()) == Counter("abcdefghijklmnopqrstuvwxyz")

class Value:
    def __init__(self, value=None, vtype=None):
        self.value = value
        self.type = vtype
    def __repr__(self):
        return f"{self.value} <TYPE {self.type}>"


class Array:
    def __init__(self, length=None, vtype=None, items=None):
        self.length = length
        self.type = vtype
        self.items = items

    def __repr__(self):
        return f"{[item for item in self.items]} <ARRAY OF {self.type}>"


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
    ############## Comandos ##############
    if isinstance(action, ast.Block):
        block = action
        new_state, return_val = evaluate(state, block.command)
        if return_val is not None:
            return new_state, return_val
        if block.next_block is not None:
            return evaluate(new_state, block.next_block)
        else:
            return new_state, 0

    elif isinstance(action, ast.AssignArray):
        array_assignment = action
        if array_assignment.id in state:
            raise VariableAlreadyDefinedError(array_assignment.id)
        candidate_array = evaluate(state, array_assignment.content)[1]
        for candidate_value in candidate_array.value.items:
            if candidate_value.type != array_assignment.type:
                raise AssignmentUnmatchedTypeError(candidate_value.type, array_assignment.type)
        if len(candidate_array.value.items) != array_assignment.length.value:
            raise ArrayLengthMismatchError(array_assignment.length.value, len(candidate_array.value.items))
        state[array_assignment.id] = candidate_array
        return state, None

    elif isinstance(action, ast.ReassignArray):
        array_reassignment = action
        if array_reassignment.id not in state:
            raise VariableNotDefinedError(array_reassignment.id)
        candidate_value = evaluate(state, array_reassignment.value)[1]
        array = state[array_reassignment.id].value
        if candidate_value.type != array.type:
            raise ReassignmentUnmatchedTypeError(candidate_value.type, array.type)
        index = evaluate(state, array_reassignment.index)[1]
        if index.type != 'int':
            raise IndexNotAnIntegerError(index)
        if index.value < 0 or index.value >= len(array.items):
            raise OutOfBoundsError(len(array.items), index.value)
        array.items[index.value] = candidate_value
        return state, None

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

    elif isinstance(action, ast.Write):
        write_command = action
        content = evaluate(state, write_command.content)[1]
        if content.type != 'string':
            raise CannotWriteNonStringToFileError(content)
        filepath_candidate = evaluate(state, write_command.file)[1]
        if filepath_candidate.type != 'string':
            raise FilePathMustBeStringError(filepath_candidate)
        filepath = Path(filepath_candidate.value)
        if filepath.exists():
            raise FileAlreadyExistsError(filepath_candidate.value)
        with open(filepath, "w") as f:
            f.write(content.value)
        return state, None

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
                    break
            else:
                break
        else:
            raise InvalidArgumentsError(func.expected(), [arg.type for arg in args])
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

    ############## Expressoes ###############
    elif isinstance(action, ast.Literal):
        literal = action
        if literal.type == "subst":
            if not is_valid_subst(literal.value):
                raise SubstNotAlphabetPermutationError(literal.value)
            literal.value = literal.value.lower()
        return state, Value(value=literal.value, vtype=literal.type)

    # Tentativa de acessar valor de variavel (ex: a)
    elif isinstance(action, str):
        var_name = action
        if var_name not in state:
            raise VariableNotDefinedError(var_name)
        return state, state[var_name]

    elif isinstance(action, ast.Array):
        array = action
        candidate_array = [evaluate(state, candidate_item)[1] for candidate_item in array.items]
        atype = candidate_array[0].type
        for candidate_item in candidate_array:
            if candidate_item.type != atype:
                raise MixedTypesInArrayError(candidate_array[0], candidate_item)
        return state, Value(vtype='array', value=Array(
            length=len(candidate_array),
            vtype=atype,
            items=candidate_array,
        ))

    elif isinstance(action, ast.GetFromArray):
        get_from_array = action
        if get_from_array.id not in state:
            raise VariableNotDefinedError(get_from_array.id)
        if state[get_from_array.id].type != 'array':
            raise NotAnArrayError(get_from_array.id)
        array = state[get_from_array.id].value
        index = evaluate(state, get_from_array.index)[1]
        if index.type != 'int':
            raise IndexNotAnIntegerError(index)
        if index.value < 0 or index.value >= len(array.items):
            raise OutOfBoundsError(len(array.items), index.value)
        return state, array.items[index.value]

    # Operacao unaria (apenas uma, ! bool)
    elif isinstance(action, ast.UnaryOp):
        v = evaluate(state, action.arg)[1]
        if action.type == "!":
            return state, Value(value= not v.value, vtype="bool")


    # Operacoes binarias (ex: a > b)
    elif isinstance(action, ast.BinOp):
        left, right = evaluate(state, action.left)[1], evaluate(state, action.right)[1]
        if left.type != right.type:
            raise SyntaxError("Tipos incompatives na operacao binop")
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

    elif isinstance(action, ast.Concat):
        concat = action
        left, right = evaluate(state, concat.left)[1], evaluate(state, concat.right)[1]
        if left.type != 'string' or right.type != 'string':
            raise InvalidTypesForConcatError(left.type, right.type)
        return state, Value(left.value + right.value, vtype='string')

    elif isinstance(action, ast.Read):
        read_command = action
        filepath_candidate = evaluate(state, read_command.file)[1]
        if filepath_candidate.type != 'string':
            raise FilePathMustBeStringError(filepath_candidate)
        filepath = Path(filepath_candidate.value)
        if not filepath.exists():
            raise FileDoesNotExistError(filepath_candidate.value)
        out = ""
        with open(filepath, "r") as f:
            out = f.read()
        return state, Value(value=out, vtype='string')

    elif isinstance(action, ast.Crypt):
        if action.type == "encode":
            encode = action
            style = evaluate(state, encode.style)[1]
            message, key = evaluate(state, encode.args[0])[1], evaluate(state, encode.args[1])[1]
            if key.type == "subst":
                if style.value == "substitution" or style.value == "vigenere":
                    out = call_encrypt_function("vigenere", message.value, key.value, "encode")
                    return state, Value(value=out, vtype='string')
                else: 
                    raise InvalidSubstTypeUse(style.type)

            out = call_encrypt_function(style.value, message.value, key.value, "encode")
            return state, Value(value=out, vtype='string')

        elif action.type == "decode":
            decode = action
            style = evaluate(state, decode.style)[1]
            message, key = evaluate(state, decode.args[0])[1], evaluate(state, decode.args[1])[1]
            value = call_encrypt_function(style.value, message.value, key.value, "decode")
            return state, Value(value=value, vtype='string')

