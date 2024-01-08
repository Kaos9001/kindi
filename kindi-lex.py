import ply.lex as lex


reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'encode': 'ENCODE',
    'decode': 'DECODE',
    'autodecode': 'AUTODECODE',
    'print': 'PRINT',
    'read': 'READ',
    'write': 'WRITE',
    'subst': 'TYPE',
    'bool': 'TYPE',
    'int': 'TYPE',
    'float': 'TYPE',
    'string': 'TYPE',
    'array': 'TYPE',
    'wordlist': 'TYPE'
}

tokens = [
    'INT',
    'BOOL',
    'FLOAT',
    'CHAR',
    'STRING',
    'SUBST',
    'ID',
    'ASSIGNMENT',
    'AND',
    'OR',
    'NOT',
    'IS_SMALLER_OR_EQUAL',
    'IS_GREATER_OR_EQUAL',
    'IS_EQUAL',
    'IS_NOT_EQUAL',
] + list(set(reserved.values()))

literals = ['+', '-', '*', '/', '{', '}', '(', ')', '[', ']', ',', '<', '>']

t_ASSIGNMENT = r'='
t_AND = r'&&'
t_OR  = r'\|\|'
t_NOT = r'!'
t_IS_SMALLER_OR_EQUAL = r'<='
t_IS_GREATER_OR_EQUAL = r'>='
t_IS_EQUAL            = r'=='
t_IS_NOT_EQUAL        = r'!='

def t_BOOL(t):
    r'True|False'
    t.value = t.value == "True"
    return t

def t_FLOAT(t):
    r'\d+\.(\d)*'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"([^"]|\\")*"'
    t.value = t.value[1:-1]
    return t

def t_SUBST(t):
    r'c"([^"]|\\")*"'
    t.value = t.value[2:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)