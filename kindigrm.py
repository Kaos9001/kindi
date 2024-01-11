import ply.yacc as yacc
from kindilex import tokens
import kindiast as ast
start = 'block'

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)

def p_block(p):
    '''block : command
             | command block'''
    if len(p) == 2: # um unico comando
        p[0] = ast.Block(command=p[1])
    else:
        p[0] = ast.Block(command=p[1], next_block=p[2])

def p_command(p):
    '''command : print
               | assign
               | reassign
               | function_call
               | conditional
               | whileloop
               | write
               | assign_array'''
    p[0] = p[1]

def p_print(p):
    '''print : PRINT '(' string_like ')' '''
    p[0] = ast.Print(content=p[3])

def p_read(p):
    '''read : READ '(' string_like ')' '''
    p[0] = ast.Read(file=p[3])

def p_write(p):
    '''write : WRITE '(' string_like ',' string_like ')' '''
    p[0] = ast.Write(file=p[3], content=p[5])

def p_assign_array(p):
    '''assign_array : TYPE ID '[' INT ']' ASSIGNMENT generics
                   | TYPE ID '[' INT ']' ASSIGNMENT array '''
    p[0] = ast.AssignArray(vtype=p[1], id=p[2], length=p[4], content=p[7])

def p_array(p):
    '''array : '[' expression next_item ']'
       next_item :
                | ',' expression next_item '''
    if len(p) == 1:
        p[0] = []
    elif p[1] == ",":
        p[0] = [p[2], *p[3]]
    elif len(p) > 3:
        p[0] = ast.Array(items=list([p[2]]) + p[3])

# TODO: acesso a arrays, indices, reassing de arrays

def p_assign(p):
    '''assign : TYPE ID ASSIGNMENT expression'''
    p[0] = ast.Assign(vtype=p[1], id=p[2], value=p[4])

def p_reassign(p):
    '''reassign : ID ASSIGNMENT expression'''
    p[0] = ast.Reassign(id=p[1], value=p[3])

def p_expression(p):
    '''expression : math_exp
                  | boolean_exp
                  | math_eval_exp
                  | string_exp
                  | literal
                  | array'''
    p[0] = p[1]

def p_literal(p):
    '''literal : ID
               | integer
               | CHAR
               | STRING
               | SUBST
               | float
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
        p[0] = ast.FunctionCall(name=p[1], args=())
    elif len(p) > 5:
        p[0] = ast.FunctionCall(name=p[1], args=tuple([p[3]]) + p[4])

def p_generics(p):
    '''generics : ID
                | function_call'''
    p[0] = p[1]

##################################################
# Sintaxe das expressões aritméticas
def p_num(p):
    '''integer : INT
              | '-' INT
        float : FLOAT
              | '-' FLOAT '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[2].value *= -1
        p[0] = p[2]

def p_math_like(p):
    '''math_like : integer
                 | float
                 | math_exp
                 | generics'''
    p[0] = p[1]

def p_math_exp(p):
    '''math_exp : math_like '+' math_like
                  | math_like '-' math_like
                  | math_like '*' math_like
                  | math_like '/' math_like
                  | '(' math_exp ')' '''
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = ast.BinOp(optype=p[2], left=p[1], right=p[3])


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
        p[0] = ast.BinOp(optype="or", left=p[1], right=p[3])
    elif p[2] == '&&':
        p[0] = ast.BinOp(optype="and", left=p[1], right=p[3])
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
        p[0] = ast.BinOp(optype="<", left=p[1], right=p[3])
    elif p[2] == '>':
        p[0] = ast.BinOp(optype=">", left=p[1], right=p[3])
    elif p[2] == '<=':
        p[0] = ast.BinOp(optype="<=", left=p[1], right=p[3])
    elif p[2] == '>=':
        p[0] = ast.BinOp(optype=">=", left=p[1], right=p[3])
    elif p[2] == '==':
        p[0] = ast.BinOp(optype="==", left=p[1], right=p[3])
    elif p[2] == '!=':
        p[0] = ast.BinOp(optype="!=", left=p[1], right=p[3])
    else:
        p[0] = p[2]

def p_not_operator(p):
    '''bool_like : NOT bool_like'''
    p[0] = ast.UnaryOp(optype="!", arg=p[2])

##################################################
# Sintaxe das expressões de string
    
# não sei ao certo este aqui, como vamos concatenar números?
# que prioridade damos a 2 + 2 + "frase"?
def p_string_exp(p):
    '''string_exp : concat
                  | read
                  | enc_dec '''
    p[0] = p[1]

def p_concat_string(p):
    '''concat : string_like '+' string_like'''
    p[0] = ast.Concat(left=p[1], right=p[3])

def p_stringlike(p):
    '''string_like : CHAR
                   | STRING
                   | string_exp
                   | generics
                   '''
    p[0] = p[1]

##################################################
# Funções reservadas
def p_encode_decode(p):
    '''enc_dec : ENCODE '<' string_like '>' '(' expression next_argument_enc ')'
               | DECODE '<' string_like '>' '(' expression next_argument_enc ')'
               | AUTODECODE '<' string_like '>' '(' expression next_argument_enc ')'
       next_argument_enc :
                         | ',' expression next_argument_enc '''
    if len(p) == 1:
        p[0] = ()
    elif p[1] == ",":
        p[0] = (p[2], *p[3])
    elif len(p) > 8:
        p[0] = ast.Crypt(ctype=p[1], style=p[3], args=tuple([p[6]]) + p[7])

##################################################

def p_conditional(p):
    '''conditional : IF '(' bool_like ')' '{' block '}' else_cond
       else_cond :
                 | ELSE '{' block '}' '''
    if len(p) == 1:
        p[0] = None
    elif p[1] == "else":
        p[0] = p[3]
    else:
        p[0] = ast.Conditional(condition=p[3], on_true=p[6], on_else=p[8])

def p_while(p):
    '''whileloop : WHILE '(' bool_like ')' '{' block '}'  '''
    p[0] = ast.While(condition=p[3], block=p[6])



# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")