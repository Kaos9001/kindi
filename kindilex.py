import ply.lex as lex

# Palavras reservadas não podem ser usadas com ID pelo usuário,
# mas podem fazer parte de IDs, e.g. "FIF" é ID válida.
# Sempre que um candidato a ID for inicializado, será checado
# se ele não é uma palavra reservada.
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
    'wordlist': 'TYPE',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIVIDE'
}

# Todos os possíveis tokens produzidos pelo lexer, a serem usados
# pelo yacc.
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

# literals = ['+', '-', '*', '/', '{', '}', '(', ')', '[', ']', ',', '<', '>']

####################################################
# Definição dos tokens
# Cada token é uma tupla (tipo, valor, número da linha, posição)
# Esses tokens são adicionados ao objeto lexer na mesma ordem
# em que aparecem no arquivo fonte.

# Os tokens mais simples serão sempre os mesmos e são definidos 
# como segue:

t_ASSIGNMENT = r'='
t_AND = r'&&'
t_OR  = r'\|\|'
t_NOT = r'!'
t_IS_SMALLER_OR_EQUAL = r'<='
t_IS_GREATER_OR_EQUAL = r'>='
t_IS_EQUAL            = r'=='
t_IS_NOT_EQUAL        = r'!='

# Tokens mais genéricos são definidos com o uso de RegEx:
# Os valores são convertidos de string para objetos de tipos
# correlatos em python, e.g. a string recebida que foi detectada como
# sendo do tipo INT da linguagem Kindi é convertida para o tipo
# int de python para ser inserida no argumento "valor" do Token.

def t_BOOL(t):
    r'True|False'
    t.value = t.value == "True"
    return t

def t_FLOAT(t):
    r'\d+\.(\d)*|\d*\.(\d)+'
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
    # É interessante mantermos uma contagem de linhas para facilitar
    # o debuging do programa.
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)