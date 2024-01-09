import ply.yacc as yacc
from kindilex import tokens

##################################################
# Semântica das expressões aritméricas
## Tipo INT
def p_factor_num(p):
    'factor : INT'
    p[0] = p[1]

def p_arithmetic_operators(p):
    '''expression : expression PLUS term
                  | expression MINUS term
       term       : term TIMES factor
                  | term DIVIDE factor'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

# Comentei porque ele reclama que não foi definido
# no lexer, mas isto aqui é muito importante, e 
# talvez tenhamos que definir LPAREN e RPAREN.
    

# com esta regra temos que as expressões são antes 
# avaliadas dentro do parenteses para então serem extraídas
# def p_factor_expr(p):
#     'factor : LPAREN expression RPAREN'
#     p[0] = p[2]

## Tipo float
# Precisamos criar a semantica separada desses dois tipos


##################################################
# Semântica das expressões lógicas
def p_bfactor_bool(p):
    'bfactor : BOOL'
    p[0] = p[1] == "True" # O lexer captura apenas 
                          # as strings "True" e "False"
                          # como booleanos.

def p_logical_operators(p):
    '''expression : bexpr OR bexpr
                  | bexpr AND bexpr'''
    if p[2] == r'\|\|':
        p[0] = p[1] or p[3]
    elif p[2] == '&&':
        p[0] = p[1] and p[3]

def p_bfactor_arithmetic(p):
    '''bfactor : INT < INT
               | INT > INT
               | INT <= INT
               | INT >= INT
               | INT == INT
               | INT != INT'''
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
    '''bfactor : ! bfactor'''
    p[0] = not p[1]

    
# def p_bfactor_bexpr(p):
#     'factor : LPAREN expression RPAREN'
#     p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()