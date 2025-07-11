import ply.yacc as yacc
import os
from datetime import datetime
from contextlib import redirect_stdout
from pprint import pprint
# Get the token map from the lexer.  This is required.
from lexico import tokens
from lexico import lexer

#Regla inicial 
start = 'program'

def p_program(p):
    '''program : declaration_list'''
    p[0] = ("program", p[1])

def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_declaration(p):
    '''declaration : class
                   | function_declaration
                   | variable_declaration SEMICOLON
                   | import_statement
                   | const_declaration SEMICOLON'''
    p[0] = p[1]

def p_import_statement(p):
    '''import_statement : IMPORT STRING_LITERAL SEMICOLON'''
    full_string = "".join(val for _, val in p[2])
    p[0] = ('import', full_string)

def p_const_declaration(p):
    '''const_declaration : CONST declaration_type ID EQUALS expression'''
    p[0] = ('const_declaration', p[2], p[3], p[5])

# -------- ELEMENTOS BASICOS  --------#
# BARZOLA LEIDY  
# Reglas de precedencia 
precedence = (
    ('right', 'EQUALS', 'PLUSEQ', 'MINUSEQ', 'TIMESEQ', 'DIVEQ', 'NULLASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQEQ', 'NEQ'),
    ('nonassoc', 'MINSIGN', 'MAXSIGN', 'MINSIGNEQ', 'MAXSIGNEQ', 'IS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'INTDIV', 'MODULE'),
    ('right', 'ELSE'),
    ('right', 'U_NOT', 'UMINUS'),
    ('left', 'PLUSPLUS', 'MINUSMINUS'),
    ('left', 'DOT', 'LBRACKET', 'LPAREN'),
    ('left', 'NOT'), # For postfix null-assert
)

#CLASES, PROPIEDADES Y MÉTODOS (Alejandro Sornoza)
def p_class(p):
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
                    | function_declaration
                    | constructor_declaration'''
    p[0] = p[1]

def p_function_declaration(p):
    '''function_declaration : declaration_type function_name LPAREN parameters RPAREN LBRACE body RBRACE'''
    p[0] = ("function", p[1], p[2], p[4], p[7])

def p_function_name(p):
    '''function_name : ID
                     | MAIN'''
    p[0] = p[1]

def p_class_property(p):
    'class_property : declaration_type ID SEMICOLON'
    p[0] = ("property", p[1], p[2])

def p_constructor_declaration(p):
    '''constructor_declaration : ID LPAREN constructor_params RPAREN SEMICOLON'''
    p[0] = ('constructor', p[1], p[3])

def p_constructor_params(p):
    '''constructor_params : constructor_param_list
                          | empty'''
    p[0] = p[1] if p[1] else []

def p_constructor_param_list(p):
    '''constructor_param_list : constructor_param_list COMMA constructor_param
                              | constructor_param'''
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_constructor_param(p):
    '''constructor_param : THIS DOT ID'''
    p[0] = ('this', p[3])

def p_declaration_type(p):
    '''declaration_type : primitive_type
                        | generic_type
                        | type_nullable
                        | ID'''
    p[0] = p[1]

def p_primitive_type(p):
    '''primitive_type : INT
                      | DOUBLE
                      | STRING
                      | BOOL
                      | VOID
                      | VAR
                      | DYNAMIC'''
    p[0] = ('type', p[1])

def p_generic_type(p):
    '''generic_type : ID MINSIGN type_list MAXSIGN'''
    p[0] = ('generic', p[1], p[3])

def p_type_nullable(p):
    'type_nullable : primitive_type QMARK'
    p[0] = ('nullable_type', p[1])

def p_expression_nullcoalescing(p):
    'expression : expression NULLCOALESCING expression'
    p[0] = ('null_coalescing', p[1], p[3])

def p_type_list(p):
    '''type_list : type_list COMMA declaration_type
                 | declaration_type'''
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]



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

def p_expression_type_check(p):
    '''expression : expression IS declaration_type
                  | expression IS NOT declaration_type'''
    if len(p) == 4:
        p[0] = ('is', p[1], p[3])
    else: # is not
        p[0] = ('is!', p[1], p[4])

def p_expression_not(p): #Alejandro Sornoza
    'expression : NOT expression %prec U_NOT'
    p[0] = ('not', p[2])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('uminus', p[2])

def p_expression_postfix(p):
    '''expression : expression PLUSPLUS
                  | expression MINUSMINUS'''
    p[0] = ('postfix', p[2], p[1])

def p_expression_member_access(p):
    'expression : expression DOT ID'
    p[0] = ('member_access', p[1], p[3])

def p_expression_subscript(p):
    'expression : expression LBRACKET expression RBRACKET'
    p[0] = ('subscript', p[1], p[3])

def p_expression_call(p):
    'expression : expression LPAREN arguments RPAREN'
    p[0] = ('call', p[1], p[3])

def p_arguments(p):
    '''arguments : expression_list
                 | empty'''
    p[0] = p[1]

def p_expression_null_assert(p):
    'expression : expression NOT'
    p[0] = ('null_assert', p[1])

def p_expression_binaria(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression INTDIV expression
                  | expression MODULE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_static_call(p):
    'factor : primitive_type DOT ID LPAREN arguments RPAREN'
    p[0] = ('static_call', p[1], p[3], p[5])

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_string(p):
    'factor : STRING_LITERAL'
    p[0] = p[1]

def p_factor_id(p):
    '''factor : ID
               | TRUE
               | FALSE'''
    if p[1] in ('true', 'false'):
        p[0] = ('bool_lit', p[1])
    else:
        p[0] = ("var", p[1])

def p_factor_expr_group(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Instrucciones
def p_instructions(p):
    '''instructions : instruction instructions
                    | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_instruction(p):
    '''instruction : variable_declaration SEMICOLON
                   | expression SEMICOLON
                   | print_statement
                   | if_else
                   | while_loop
                   | for_loop
                   | return_statement
                   | block_statement
                   | throw_statement
                   | try_statement
                   | const_declaration SEMICOLON
                   | break_statement
                   | continue_statement'''
    p[0] = p[1]

def p_try_statement(p):
    '''try_statement : TRY block_statement catch_clauses
                     | TRY block_statement catch_clauses finally_clause
                     | TRY block_statement finally_clause'''
    if len(p) == 4:
        if p[3] is None or isinstance(p[3], list):
            # try + block + catch(es)
            p[0] = ('try', p[2], p[3], None)
        else:
            # try + block + finally
            p[0] = ('try', p[2], [], p[3])
    else:
        # try + block + catch(es) + finally
        p[0] = ('try', p[2], p[3], p[4])

def p_catch_clauses(p):
    '''catch_clauses : catch_clauses catch_clause
                     | catch_clause'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_catch_clause(p):
    '''catch_clause : CATCH LPAREN ID RPAREN block_statement
                    | CATCH LPAREN ID ID RPAREN block_statement'''
    if len(p) == 6:
        # catch (e) { ... }
        p[0] = ('catch', None, p[3], p[5])
    else:
        # catch (ExceptionType e) { ... }
        p[0] = ('catch', p[3], p[4], p[6])

def p_finally_clause(p):
    'finally_clause : FINALLY block_statement'
    p[0] = p[2]


def p_block_statement(p):
    'block_statement : LBRACE instructions RBRACE'
    p[0] = ('block', p[2])

def p_throw_statement(p):
    'throw_statement : THROW expression SEMICOLON'
    p[0] = ('throw', p[2])

# Asignaciones
def p_variable_declaration(p):
    '''variable_declaration : declaration_type ID
                            | declaration_type ID EQUALS expression'''
    if len(p) == 3:
        p[0] = ('variable_declaration', p[1], p[2], None)
    else:
        p[0] = ('variable_declaration', p[1], p[2], p[4])

def p_expression_assignment(p):
    '''expression : expression EQUALS expression
                  | expression PLUSEQ expression
                  | expression MINUSEQ expression
                  | expression TIMESEQ expression
                  | expression DIVEQ expression
                  | expression NULLASSIGN expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_ternary(p): #Alejandro Sornoza
    '''expression : expression QMARK expression COLON expression'''
    p[0] = ("ternary", p[1], p[3], p[5])


# Impresion 
def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = ("print", p[3])

#Parametros
def p_parameters(p):
    '''parameters : parameters COMMA declaration_type ID
                  | declaration_type ID
                  | empty'''
    if len(p) == 5:
        p[0] = p[1] + [(p[3], p[4])]
    elif len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = []

#Return
def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    if len(p) == 4:
        p[0] = ("return", p[2])
    else:
        p[0] = ("return", None)


# -------- ESTRUCTURAS AVANZADAS --------#
#FUNCIONES
def p_body(p):
    '''body : instructions'''
    p[0] = p[1]




#ESTRUCTURA DE CONTROL 
# If-else - Barzola Leidy 
def p_if_else(p):
    '''if_else : IF LPAREN expression RPAREN instruction
               | IF LPAREN expression RPAREN instruction ELSE instruction'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])

#While Alejandro Sornoza
def p_while_loop(p):
    'while_loop : WHILE LPAREN expression RPAREN instruction'
    p[0] = ("while", p[3], p[5])

#For Alejandro Sornoza
def p_for_loop(p):
    'for_loop : FOR LPAREN for_initializer SEMICOLON expression_opt SEMICOLON expression_opt RPAREN instruction'
    p[0] = ('for', p[3], p[5], p[7], p[9])

def p_for_initializer(p):
    '''for_initializer : variable_declaration
                       | expression
                       | empty'''
    p[0] = p[1]

def p_expression_opt(p):
    '''expression_opt : expression
                      | empty'''
    p[0] = p[1]

#ESTRUCTURA DE DATOS
# Arrays - Barzola Leidy  
def p_expression_array(p):
    'expression : LBRACKET expression_list RBRACKET'
    p[0] = ("array", p[2])

#HILDA ANGULO
# Sets and Maps 
def p_expression_set_or_map(p):
    'expression : LBRACE set_or_map_contents RBRACE'
    p[0] = p[2]

def p_set_or_map_contents(p):
    '''set_or_map_contents : expression set_or_map_tail
                           | empty'''
    if len(p) == 2:
        # Empty {} is a map by default in Dart
        p[0] = ('map', [])
    else:
        first_element = p[1]
        type, tail_elements = p[2]
        if type == 'map':
            first_value = tail_elements.pop(0)
            first_entry = (first_element, first_value)
            p[0] = ('map', [first_entry] + tail_elements)
        else: # type == 'set'
            p[0] = ('set', [first_element] + tail_elements)

def p_set_or_map_tail(p):
    '''set_or_map_tail : COLON expression map_tail
                       | set_tail'''
    if len(p) == 4: # It's a map
        p[0] = ('map', [p[2]] + p[3])
    else: # It's a set
        p[0] = ('set', p[1])

def p_map_tail(p):
    '''map_tail : COMMA map_entries
                | empty'''
    p[0] = p[2] if len(p) == 3 else []

def p_map_entries(p):
    '''map_entries : map_entries COMMA map_entry
                   | map_entry'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_map_entry(p):
    'map_entry : expression COLON expression'
    p[0] = (p[1], p[3])

def p_set_tail(p):
    '''set_tail : COMMA expression_list
                | empty'''
    p[0] = p[2] if len(p) == 3 else []

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

def p_break_statement(p):
    'break_statement : BREAK SEMICOLON'
    p[0] = ('break',)

def p_continue_statement(p):
    'continue_statement : CONTINUE SEMICOLON'
    p[0] = ('continue',)

# Vacío
def p_empty(p):
    'empty :'
    p[0] = []

# Error 
def p_error(p):
    if p:
        print(f"Syntax error at token '{p.type}' with value '{p.value}'")
    else:
        print("Syntax error at end of input")

# Build the parser
parser = yacc.yacc()

# Mapeo de archivos a usuarios Git
archivos_usuarios = {
    "algoritmo1.dart": "ljbarzol",
    "algoritmo2.dart": "vic28code",
    "algoritmo3.dart": "AlejandroSV2004"
}

# Crear carpeta de logs si no existe
carpeta_logs = "logsSintax"
os.makedirs(carpeta_logs, exist_ok=True)

# Fecha y hora actual para el lote de análisis
fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")

# Procesar cada archivo y generar su log individual
for archivo, usuario in archivos_usuarios.items():
    nombre_log = f"sintactico-{usuario}-{fecha_hora}.txt"
    ruta_log = os.path.join(carpeta_logs, nombre_log)
    
    try:
        with open("algoritmos/"+archivo, 'r', encoding='utf-8') as f_in:
            data = f_in.read()

        print(f"Analizando {archivo}...")
        with open(ruta_log, "w", encoding="utf-8") as log_file:
            log_file.write(f"--- Análisis de: {archivo} (Usuario: {usuario}) ---\n\n")
            with redirect_stdout(log_file):
                # Reset lexer state for each file
                lexer.lineno = 1
                result = parser.parse(data, lexer=lexer)
                if result:
                    print("\n--- Resultado del Análisis (AST) ---")
                    pprint(result)

    except FileNotFoundError:
        # Log if the source file wasn't found
        with open(ruta_log, "w", encoding="utf-8") as log_file:
            log_file.write(f"Error: El archivo de entrada '{archivo}' no fue encontrado.")
        print(f"Error: El archivo de entrada '{archivo}' no fue encontrado.")
    except Exception as e:
        # Log any other exceptions
        with open(ruta_log, "w", encoding="utf-8") as log_file:
            log_file.write(f"Ocurrió un error inesperado al procesar {archivo}: {e}")
        print(f"Ocurrió un error inesperado al procesar {archivo}: {e}")
    
    print(f"Log generado: {ruta_log}")

def analizar_sintactico(codigo):
    from lexico import lexer  # Asegúrate de importar el lexer
    errores = []  # Guarda los mensajes de error

    def custom_error(p):
        if p:
            errores.append(f"Error de sintaxis: token '{p.type}' con valor '{p.value}'")
        else:
            errores.append("Error de sintaxis: fin de entrada inesperado")

    # Construye un parser nuevo con la función de error personalizada
    parser = yacc.yacc()
    parser.errorfunc = custom_error

    lexer.lineno = 1
    try:
        result = parser.parse(codigo, lexer=lexer)
        if result:
            return ["Todo está bien: sin errores sintácticos."]
        else:
            if errores:
                return errores
            else:
                return ["No se generó AST. Revisa paréntesis, operadores y puntos y coma."]
    except Exception as e:
        return [f"Error sintáctico: {e}"]

