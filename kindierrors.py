class VariableAlreadyDefinedError(Exception):
    pass

class VariableNotDefinedError(Exception):
    pass

class ReassignmentUnmatchedTypeError(Exception):
    pass

class AssignmentUnmatchedTypeError(Exception):
    pass

class InvalidTypeForPrintError(Exception):
    pass

class InvalidTypesForConcatError(Exception):
    pass

class UndefinedIsNotAFunctionError(Exception):
    pass

class NotAFunctionError(Exception):
    pass

class IncorrectNumberOfArgumentsError(Exception):
    pass

class InvalidArgumentsError(Exception):
    pass

class ReservedWordInArgumentsError(Exception):
    pass