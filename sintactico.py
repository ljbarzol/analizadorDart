import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexico import tokens
from lexico import lexer

#Regla inicial 
start = 'program'

def p_program(p):
    '''program : classes functions
               | instructions'''
    if len(p) == 3:
        p[0] = ("program", p[1], p[2])
    else:
        p[0] = ("program", p[1])


def p_classes(p):
    '''classes : class classes
               | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


# -------- ELEMENTOS BASICOS  --------#
# BARZOLA LEIDY  
# Reglas de precedencia 
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

#INPUT (Alejandro Sornoza)
def p_input_statement(p):
    '''expression : ID DOT ID LPAREN RPAREN'''
    p[0] = ("input", f"{p[1]}.{p[3]}")

#CLASES, PROPIEDADES Y MÉTODOS (Alejandro Sornoza)
def p_class_declaration(p):
    '''class : CLASS ID LBRACE class_body RBRACE'''
    p[0] = ("class", p[2], p[4])

def p_class_body(p):
    '''class_body : class_member class_body
                  | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_class_member(p):
    '''class_member : class_property
                    | method'''
    p[0] = p[1]

def p_method(p):
    '''method : type ID LPAREN parameters RPAREN LBRACE body return_statement RBRACE'''
    p[0] = ("method", p[1], p[2], p[4], p[6], p[7])

def p_class_property(p):
    'class_property : type ID SEMICOLON'
    p[0] = ("property", p[1], p[2])

def p_type(p):
    '''type : INT
            | DOUBLE
            | STRING
            | BOOL
            | VOID'''
    p[0] = p[1]



# Expresiones
def p_expression_logical(p): #Alejandro Sornoza
    '''expression : expression AND expression
                  | expression OR expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_relational(p): #Alejandro Sornoza
    '''expression : expression EQEQ expression
                  | expression NEQ expression
                  | expression MINSIGN expression
                  | expression MAXSIGN expression
                  | expression MINSIGNEQ expression
                  | expression MAXSIGNEQ expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_not(p): #Alejandro Sornoza
    'expression : NOT expression'
    p[0] = ('not', p[2])

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

def p_assignment_typed(p): #Alejandro Sornoza
    '''assignment : type ID EQUALS expression SEMICOLON'''
    p[0] = ("typed_assign", p[1], p[2], p[4])

def p_expression_ternary(p): #Alejandro Sornoza
    '''expression : expression QMARK expression COLON expression'''
    p[0] = ("ternary", p[1], p[3], p[5])


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
def p_function_with_return(p):
    'function_with_return : type ID LPAREN parameters RPAREN LBRACE body return_statement RBRACE'
    p[0] = ("function_with_return", p[1], p[2], p[4], p[7], p[8])

def p_main_function(p):
    'main_function : VOID MAIN LPAREN RPAREN LBRACE body RBRACE'
    p[0] = ("main_function", p[6])


def p_function(p):
    '''function : function_with_return
                | main_function'''
    p[0] = p[1]


def p_functions(p):
    '''functions : function functions
                 | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_body(p):
    '''body : instructions'''
    p[0] = p[1]




#ESTRUCTURA DE CONTROL 
# If-else - Barzola Leidy 
def p_if_else(p):
    'if_else : IF LPAREN expression RPAREN LBRACE instructions RBRACE ELSE LBRACE instructions RBRACE'
    p[0] = ("if_else", p[3], p[6], p[10])

#While Alejandro Sornoza
def p_while_loop(p):
    'instruction : WHILE LPAREN expression RPAREN LBRACE instructions RBRACE'
    p[0] = ("while", p[3], p[6])

#For Alejandro Sornoza
def p_for_loop(p):
    'instruction : FOR LPAREN assignment expression SEMICOLON assignment RPAREN LBRACE instructions RBRACE'
    p[0] = ("for", p[3], p[4], p[6], p[9])

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
    result = parser.parse(s, lexer=lexer)
    print(result)