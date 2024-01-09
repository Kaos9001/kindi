import ply.yacc as yacc
from kindilex import tokens
functions = {}

start = 'expression'
def p_expression(p):
    '''expression : math_exp
                  | boolean_exp
                  | literal'''
    p[0] = p[1]

def p_literal(p):
    '''literal : ID
               | INT
               | CHAR
               | STRING
               | SUBST
               | FLOAT
               | BOOL'''
    p[0] = p[1]

def p_function_call(p):
    '''function_call : ID '(' expression next_argument ')'
       next_argument :
                     | ',' expression next_argument'''
    p[0] = functions[p[1]](*p[3:len(p)-1])
def p_generics(p):
    '''generics : ID
                | function_call'''
    p[0] = p[1]

##################################################
# Semântica das expressões aritméricas
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

def p_arithmetic_operators(p):
    '''math_exp : math_like '+' math_like
                  | math_like '-' math_like
                  | math_like '*' math_like
                  | math_like '/' math_like
                  | '(' math_exp ')' '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

## Tipo float
# Precisamos criar a semantica separada desses dois tipos


##################################################
# Semântica das expressões lógicas
def p_bfactor_bool(p):
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
                  | bool_like AND bool_like'''
    if p[2] == r'\|\|':
        p[0] = p[1] or p[3]
    elif p[2] == '&&':
        p[0] = p[1] and p[3]

def p_math_eval_exp(p):
    '''math_eval_exp : math_like '<' math_like
                     | math_like '>' math_like
                     | math_like IS_LESSER_OR_EQUAL math_like
                     | math_like IS_EQUAL math_like
                     | math_like IS_NOT_EQUAL math_like'''
    if p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]

def p_not_operator(p):
    '''bool_like : NOT bool_like'''
    p[0] = not p[2]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")