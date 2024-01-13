import ply.lex as lex
import kindiast as ast

# Palavras reservadas não podem ser usadas com ID pelo usuário,
# mas podem fazer parte de IDs, e.g. "ifelse" é ID válida.
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
    'function' : "FUNCTION_DEF",
    'return' : "RETURN",
    'subst': 'TYPE',
    'bool': 'TYPE',
    'int': 'TYPE',
    'float': 'TYPE',
    'string': 'TYPE',
    'array': 'TYPE',
    'wordlist': 'TYPE',
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
    'IS_LESSER_OR_EQUAL',
    'IS_GREATER_OR_EQUAL',
    'IS_EQUAL',
    'IS_NOT_EQUAL',
] + list(set(reserved.values()))

literals = ['+', '-', '*', '/', '{', '}', '(', ')', '[', ']', ',', '<', '>']

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
t_IS_LESSER_OR_EQUAL = r'<='
t_IS_GREATER_OR_EQUAL = r'>='
t_IS_EQUAL            = r'=='
t_IS_NOT_EQUAL        = r'!='

# Tokens mais genéricos são definidos com o uso de RegEx:
# Os valores são convertidos de string para objetos que encapsulam
# seu tipo para futuro processamento

def t_COMMENT(t):
    r'\#.*'
    pass

def t_BOOL(t):
    r'True|False'
    t.value = ast.Literal(ltype="bool", value=(t.value == "True"))
    return t

def t_FLOAT(t):
    r'\d+\.(\d)*|\d*\.(\d)+'
    t.value = ast.Literal(ltype="float", value=float(t.value))
    return t

def t_INT(t):
    r'\d+'
    t.value = ast.Literal(ltype="int", value=int(t.value))
    return t

def t_STRING(t):
    r'"([^"]|\\")*"'
    t.value = ast.Literal(ltype="string", value=t.value[1:-1])
    return t

def t_SUBST(t):
    r'c"([^"]|\\")*"'
    t.value = ast.Literal(ltype="subst", value=t.value[2:-1])
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    #if t.type == 'ID':
    #    t.value = ast.ID(id=t.value)
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