import ply.lex as lex

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   #Hilda Angulo
   'int' : 'INT',
   'double' : 'DOUBLE',
   'bool' : 'BOOL',
   'String' : 'STRING',
   'class': 'CLASS',
   'extends': 'EXTENDS',
   'implements': 'IMPLEMENTS',
   'return': 'RETURN',
   'import': 'IMPORT',
   'const': 'CONST',
   'final': 'FINAL'
}

tokens = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'LBRACES',
    'RBRACES',
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
    'INTDIV'
] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACES = r'{'
t_RBRACES = r'}'
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



def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
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
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Crear analizador léxico
lexer = lex.lex()

archivos = ['algoritmo1.dart', 'algoritmo2.dart']

for nombre in archivos:
    with open(nombre, 'r', encoding='utf-8') as archivo:
        data = archivo.read()
        print(f"\nTokens de {nombre}:")
        lexer.input(data)
        for tok in lexer:
            print(tok)


#PRUEBA 
lexer.input(data)

#Imprimir los token generados(por arreglar para ponerlo en log)
print("Tokens encontrados:")
for tok in lexer:
    print(tok)

