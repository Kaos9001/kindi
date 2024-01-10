import ply.yacc as yacc
from kindilex import tokens
functions = {}

start = 'block'

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)

def p_block(p):
    '''block : command
             | block command'''
    if len(p) == 2: # um unico comando
        p[0] = ("block", p[1],)
    else:
        p[0] = p[1] + (p[2],) #adicionar os proximos comandos na sequencia

def p_command(p):
    '''command : print
               | assign
               | reassign
               | function_call'''
    p[0] = p[1]

def p_print(p):
    '''print : PRINT '(' string_like ')' '''
    p[0] = ("print", p[3])

def p_assign(p):
    '''assign : TYPE ID ASSIGNMENT expression'''
    p[0] = ("assign", p[1], p[2], p[4])

def p_reassign(p):
    '''reassign : ID ASSIGNMENT expression'''
    p[0] = ("reassign", p[1], p[3])

def p_expression(p):
    '''expression : math_exp
                  | boolean_exp
                  | math_eval_exp
                  | string_exp
                  | literal'''
    p[0] = p[1]

# isso de literal ta certo? ele ta convertendo 2 em literal
# n sei se o nome literal ta certo, mas de qqr forma
# colocar 'ID' resolva os problemas
def p_literal(p):
    '''literal : ID
               | INT
               | CHAR
               | STRING
               | SUBST
               | FLOAT
               | BOOL '''
    p[0] = p[1]


def p_function_call(p):
    '''function_call : ID '(' expression next_argument ')'
                     | ID '(' ')'
       next_argument :
                     | ',' expression next_argument '''
    if len(p) == 1:
        p[0] = ()
    elif p[1] == ",":
        p[0] = (p[2], *p[3])
    elif len(p) == 4:
        p[0] = ("call", p[1], ())
    elif len(p) > 5:
        p[0] = ("call", p[1], tuple([p[3]]) + p[4])

def p_generics(p):
    '''generics : ID
                | function_call'''
    p[0] = p[1]

# depois colocamos a tipagem

##################################################
# Sintaxe das expressões aritméricas
## Tipo INT
def p_int_num(p):
    '''integer : INT
              | '-' INT '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = -p[2]

def p_math_like(p):
    '''math_like : integer
                 | math_exp
                 | generics'''
    p[0] = p[1]

def p_math_exp(p):
    '''math_exp : math_like '+' math_like
                  | math_like '-' math_like
                  | math_like '*' math_like
                  | math_like '/' math_like
                  | '(' math_exp ')' '''
    if p[2] == '+':
        p[0] = ("sum", p[1], p[3])
    elif p[2] == '-':
        p[0] = ("sub", p[1], p[3])
    elif p[2] == '*':
        p[0] = ("mult", p[1], p[3])
    elif p[2] == '/':
        p[0] = ("div", p[1], p[3])
    else:
        p[0] = p[2]

## Tipo float
# Precisamos criar a semantica separada desses dois tipos


##################################################
# Sintaxe das expressões lógicas
def p_bool_bool(p):
    '''bool : BOOL'''
    p[0] = p[1]

def p_bool_like(p):
    '''bool_like : bool
                 | boolean_exp
                 | math_eval_exp
                 | generics'''
    p[0] = p[1]

def p_boolean_exp(p):
    '''boolean_exp : bool_like OR bool_like
                  | bool_like AND bool_like
                  | '(' boolean_exp ')' '''
    if p[2] == r'\|\|':
        p[0] = ("or", p[1], p[3]) #p[1] or p[3]
    elif p[2] == '&&':
        p[0] = ("and", p[1], p[3])
    else:
        p[0] = p[2]

def p_math_eval_exp(p):
    '''math_eval_exp : math_like '<' math_like
                     | math_like '>' math_like
                     | math_like IS_LESSER_OR_EQUAL math_like
                     | math_like IS_GREATER_OR_EQUAL math_like
                     | math_like IS_EQUAL math_like
                     | math_like IS_NOT_EQUAL math_like
                     | '(' math_eval_exp ')' '''
    # p[0] = (p[2], p[1], p[3])
    if p[2] == '<':
        p[0] = ("<", p[1], p[3]) #p[1] < p[3]
    elif p[2] == '>':
        p[0] = (">", p[1], p[3]) #p[1] > p[3]
    elif p[2] == '<=':
        p[0] = ("<=", p[1], p[3]) #p[1] <= p[3]
    elif p[2] == '>=':
        p[0] = (">=", p[1], p[3]) #p[1] >= p[3]
    elif p[2] == '==':
        p[0] = ("==", p[1], p[3]) #p[1] == p[3]
    elif p[2] == '!=':
        p[0] = ("!=", p[1], p[3]) #p[1] != p[3]
    else:
        p[0] = p[2]

def p_not_operator(p):
    '''bool_like : NOT bool_like'''
    p[0] = ("!", p[2])

##################################################
# Sintaxe das expressões de string
    
# não sei ao certo este aqui, como vamos concatenar números?
# que prioridade damos a 2 + 2 + "frase"?
def p_concat_string(p):
    '''string_exp : string_like '+' string_like'''
    p[0] = ("concat", p[1], p[3])

# Esta incompleto, fala ainda concat encode decode autodecode
def p_stringlike(p):
    '''string_like : CHAR
                   | STRING
                   | enc_dec
                   | generics
                   '''
    p[0] = p[1]

##################################################
# Chamada de Função

# Temos que ver como fazer a chamada aceitar uma 
# quantidade arbitraria de argumentos
    
# def p_function_call(p):
#     '''fucntion_call : ID '''


# Funções reservadas
def p_encode_decode(p):
    '''enc_dec : ENCODE '<' string_like '>' '(' expression next_argument_enc ')'
               | DECODE '<' string_like '>' '(' expression next_argument_enc ')'
       next_argument_enc :
                     | ',' expression next_argument_enc '''
    if len(p) == 1:
        p[0] = ()
    elif p[1] == ",":
        p[0] = (p[2], *p[3])
    elif len(p) == 7:
        p[0] = (p[1], p[3], ())
    elif len(p) > 8:
        p[0] = (p[1], p[3], tuple([p[6]]) + p[7])

##################################################
# Laço while
# def p_while(p):
#     '''loop : WHILE '(' bool_like '{' block '}' ')' '''
#     p[0] = ('while', p[2], p[4])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")