import ply.lex as lex

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
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

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Crear analizador léxico
lexer = lex.lex()

with open('algoritmo1.dart', 'r', encoding='utf-8') as archivo:
    data = archivo.read()

#PRUEBA 
lexer.input(data)

#Imprimir los token generados(por arreglar para ponerlo en log)
print("Tokens encontrados:")
for tok in lexer:
    print(tok)