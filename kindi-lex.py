import ply.lex as lex


reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'encode': 'ENCODE',
    'decode': 'DECODE',
    'print': 'PRINT',
    'read': 'READ',
    'write': 'WRITE',
    'subst': 'TYPE',
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
    'ORDER_OP',
    'LOGIC_OP',
] + list(set(reserved.values()))

literals = ['+', '-', '*', '/', '{', '}', '(', ')', '[', ']', '!']

def t_BOOL(t):
    r'^True$|^False$'
    t.value = t.value == "True"
    return t


# def t_ORDER_OP(t):
#     pass

def t_FLOAT(t):
    r'\d+\.\d?'
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
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)