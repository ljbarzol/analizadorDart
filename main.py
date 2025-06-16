import ply.yacc as yacc
from lexico import tokens

def p_program(p):
    '''program : function_list
               | '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_function_list(p):
    '''function_list : function function_list
                     | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_function(p):
    '''function : type ID LPAREN parameters RPAREN block'''
    p[0] = ('function', p[1], p[2], p[4], p[6])

def p_parameters(p):
    '''parameters : parameter_list
                  | '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_parameter_list(p):
    '''parameter_list : parameter COMMA parameter_list
                      | parameter
                      | '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_parameter(p):
    '''parameter : type ID'''
    p[0] = (p[1], p[2])


#def p_cuerpo(p):
   # '''cuerpo : lineas
 #   | lineas cuerpo'''

#def p_lineas(p):
   # '''lineas : assignment
   # | expression '''

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_block(p):
    '''block : LBRACES statements RBRACES'''
    p[0] = p[2]

def p_statements(p):
    '''statements : statement statements
                  | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_statement(p):
    '''statement : expression SEMICOLON'''
    p[0] = p[1]

def p_type(p):
    '''type : INT
            | DOUBLE
            | BOOL
            | STRING
            | VAR'''
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)