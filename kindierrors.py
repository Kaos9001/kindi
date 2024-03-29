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

class NotAnArrayError(Exception):
    pass

class OutOfBoundsError(Exception):
    pass

class MixedTypesInArrayError(Exception):
    pass

class ArrayLengthMismatchError(Exception):
    pass

class IndexNotAnIntegerError(Exception):
    pass

class CannotWriteNonStringToFileError(Exception):
    pass

class FilePathMustBeStringError(Exception):
    pass

class FileAlreadyExistsError(Exception):
    pass

class FileDoesNotExistError(Exception):
    pass

class NonStringInWordlistError(Exception):
    pass

class EncryptionKeyLenError(Exception):
    pass

class SubstNotAlphabetPermutationError(Exception):
    pass

class InvalidSubstTypeUse(Exception):
    pass