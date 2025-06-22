import os
from datetime import datetime
import ply.lex as lex

#FUNCIONES

#Leidy Barzola

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

#Hilda Angulo

def t_COMMENT(t):
    r'//.*'
    pass

def t_STRING_LITERAL(t):
    r'\"([^\\\"]|\\.)*\"|\'([^\\\']|\\.)*\''
    import re
    raw = t.value[1:-1]
    parts = re.split(r'(\$[a-zA-Z_][a-zA-Z0-9_]*)', raw)
    t.value = []
    for part in parts:
        if part.startswith('$'):
            t.value.append(('var', part[1:]))  # elimina el '$'
        else:
            t.value.append(('str', part))
    return t



#Alejandro Sornoza

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_COMMENT_MULTILINE(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    t.lexer.lineno += t.value.count('\n')  # Actualiza número de línea
    pass


#PALABRAS RESERVADAS 
reserved = {
   #Leidy Barzola
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'dynamic': 'DYNAMIC',
   'is': 'IS',
   #Hilda Angulo
   'int' : 'INT',
   'double' : 'DOUBLE',
   'bool' : 'BOOL',
   'String' : 'STRING',
   'class': 'CLASS',
   'extends': 'EXTENDS',
   'implements': 'IMPLEMENTS',
   'void' : 'VOID',
   'main' : 'MAIN',
   'return': 'RETURN',
   'import': 'IMPORT',
   'const': 'CONST',
   'final': 'FINAL',
   'this': 'THIS',
   'throw': 'THROW',
   #Alejandro Sornoza
   'for':'FOR',
   'var': 'VAR',
   'switch': 'SWITCH',
   'case': 'CASE',
   'break': 'BREAK',
   'continue': 'CONTINUE',
   'print': 'PRINT'
}

#TOKENS
tokens = [
    #Leidy Barzola
    'DOT',
    'COMMA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SQUOTE',
    'ID',
    'NUMBER',
    #Hilda Angulo
    'EQEQ',
    'NEQ',
    'MINSIGN',
    'MAXSIGN',
    'AND',
    'OR',
    'COMMENT',
    'STRING_LITERAL',
    'MODULE',
    'COLON',
    'SEMICOLON',
    'NOT',
    'INTDIV',
    'DYNAMIC',
    'IS',
    #Alejandro Sornoza
    'PLUSEQ',
    'MINUSEQ',
    'TIMESEQ',
    'DIVEQ',
    'NULLASSIGN',
    'MINSIGNEQ',
    'MAXSIGNEQ',
    'QMARK_DOT',
    'NULLCOALESCING',
    'LBRACKET',
    'RBRACKET',
    'QMARK',
    'PLUSPLUS',
    'MINUSMINUS',
    'THIS',
    'THROW'
] + list(reserved.values())

t_DOT = r'\.'
t_COMMA = r'\,'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SQUOTE = r'\''
#Hilda Angulo
t_EQEQ = r'=='
t_NEQ = r'!='
t_MINSIGN = r'<'
t_MAXSIGN = r'>'
t_AND = r'&&'
t_OR = r'\|\|'
t_MODULE = r'%'
t_COLON = r':'
t_SEMICOLON = r';'
t_NOT= r'!'
t_INTDIV = r'~\/'
#Alejandro Sornoza
t_QMARK = r'\?'
t_PLUSEQ = r'\+='
t_MINUSEQ = r'-='
t_TIMESEQ = r'\*='
t_DIVEQ = r'/='
t_NULLASSIGN = r'\?\?='
t_MINSIGNEQ = r'<='
t_MAXSIGNEQ = r'>='
t_QMARK_DOT = r'\?\.'
t_NULLCOALESCING = r'\?\?'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'


#Crear analizador léxico
lexer = lex.lex()

archivos = ['algoritmo1.dart', 'algoritmo2.dart', 'algoritmo3.dart']

usuarios_por_archivo = {
    'algoritmo1.dart': 'ljbarzol',
    'algoritmo2.dart': 'vic28code',
    'algoritmo3.dart': 'AlejandroSV2004'
}

carpeta_logs = "logsArchivos"
os.makedirs(carpeta_logs, exist_ok=True)

for archivo_nombre in archivos:
    with open(archivo_nombre, 'r', encoding='utf-8') as archivo:
        data = archivo.read()
        lexer.lineno = 1  
        lexer.input(data)

        usuario = usuarios_por_archivo.get(archivo_nombre, 'desconocido')
        fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
        nombre_log = f"lexico-{usuario}-{fecha_hora}.txt"
        ruta_log = os.path.join(carpeta_logs, nombre_log)

        with open(ruta_log, 'w', encoding='utf-8') as log:
            log.write(f"Tokens de {archivo_nombre}:\n")
            try:
                for tok in lexer:
                    log.write(f"{tok}\n")
            except Exception as e:
                log.write(f"Error: {e}\n")

        print(f"Log creado: {ruta_log}")
        
#PRUEBA 
lexer.input(data)
