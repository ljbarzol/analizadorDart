import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexico import tokens

#Regla inicial 
start = 'program'

def p_program(p):
    '''program : classes functions'''
    p[0] = ("program", p[1], p[2]) 

# -------- ELEMENTOS BASICOS  --------#
# BARZOLA LEIDY  
# Reglas de precedencia 
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Expresiones
def p_expression_binaria(p):
    '''expression : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_string(p):
    'factor : STRING_LITERAL'
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = ("var", p[1])

def p_factor_expr_group(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Instrucciones
def p_instructions_multiple(p):
    'instructions : instruction instructions'
    p[0] = [p[1]] + p[2]

def p_instructions_empty(p):
    'instructions : empty'
    p[0] = []

def p_instruction(p):
    '''instruction : assignment
                    | print_statement
                    | if_else'''
    p[0] = p[1]

# Asignaciones
def p_assignment(p):
    'assignment : ID EQUALS expression SEMICOLON'
    p[0] = ("assign", p[1], p[3])

# Impresion 
def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = ("print", p[3])

#Parametros
def p_parameters(p):
    '''parameters : type ID COMMA parameters
                    | type ID
                    | empty'''
    if len(p) == 3:
        p[0] = [(p[1], p[2])]
    elif len(p) == 5:
        p[0] = [(p[1], p[2])] + p[4]
    else:
        p[0] = []

#Return
def p_return_statement(p):
    'return_statement : RETURN expression SEMICOLON'
    p[0] = ("return", p[2])


# -------- ESTRUCTURAS AVANZADAS --------#
#FUNCIONES
# Funcion main - Barzola Leidy  
def p_function_main(p):
    'function : VOID MAIN LPAREN RPAREN LBRACE body RBRACE'
    p[0] = ("main_function", p[6])

# Funcion con retorno - Barzola Leidy 
def p_function_with_return(p):
    'function : type ID LPAREN parameters RPAREN LBRACE body return_statement RBRACE'
    p[0] = ("function_with_return", p[1], p[2], p[4], p[6], p[7])


#ESTRUCTURA DE CONTROL 
# If-else - Barzola Leidy 
def p_if_else(p):
    'if_else : IF LPAREN expression RPAREN LBRACE instructions RBRACE ELSE LBRACE instructions RBRACE'
    p[0] = ("if_else", p[3], p[6], p[10])

#ESTRUCTURA DE DATOS
# Arrays - Barzola Leidy  
def p_expression_array(p):
    'expression : LBRACKET expression_list RBRACKET'
    p[0] = ("array", p[2])

def p_expression_list(p):
    '''expression_list : expression COMMA expression_list
                        | expression
                        | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


# Vacío
def p_empty(p):
    'empty :'
    p[0] = []

# Error 
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('dart > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)