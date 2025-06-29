from pprint import pformat
from contextlib import redirect_stdout
from sintactico import parser, lexer
import os
from datetime import datetime

symbol_table = {}

#Analisis semantico 
def analizar(ast):
    if not ast or ast[0] != 'program':
        raise Exception("AST inválido o vacío")
    
    declaraciones = ast[1]
    for decl in declaraciones:
        analizar_declaracion(decl)

def analizar_declaracion(node):
    tipo = node[0]

    if tipo == 'variable_declaration':
        manejar_variable(node)
    elif tipo == 'const_declaration':
        manejar_variable(node, constante=True)


#Manejo de variables y constantes - Barzola 
def manejar_variable(node, constante=False):
    _, tipo_decl, nombre, valor = node
    tipo_esperado = obtener_tipo(tipo_decl)

    if nombre in symbol_table:
        raise Exception(f"Variable '{nombre}' ya está declarada.")

    if valor is not None:
        tipo_valor = evaluar_expr(valor)
        if not tipos_compatibles(tipo_esperado, tipo_valor):
            raise Exception(f"Tipo incorrecto en '{nombre}': se esperaba {tipo_esperado}, se recibió {tipo_valor}")

    symbol_table[nombre] = tipo_esperado
    print(f"[OK] {'Constante' if constante else 'Variable'} '{nombre}' declarada como {tipo_esperado}")

def obtener_tipo(tipo):
    if isinstance(tipo, tuple):
        if tipo[0] == 'type':
            return tipo[1]
        elif tipo[0] == 'nullable_type':
            return obtener_tipo(tipo[1]) + '?'
    elif isinstance(tipo, str):
        return tipo
    return "unknown"

def evaluar_expr(expr):
    if isinstance(expr, list) and len(expr) == 1:
        expr = expr[0]  # Desempaqueta listas como [('str', 'Hola Mundo')]

    if isinstance(expr, tuple):
        op = expr[0]

        if op == "var":
            nombre = expr[1]
            if nombre not in symbol_table:
                raise Exception(f"Variable no declarada: {nombre}")
            return symbol_table[nombre]
        elif op in ('+', '-', '*', '/', '//'):
            t1 = evaluar_expr(expr[1])
            t2 = evaluar_expr(expr[2])
            return promover_tipo(t1, t2)
        elif op in ("string_lit", "str"):
            return "String"
        elif op == "int_lit":
            return "int"
        elif op == "double_lit":
            return "double"
        elif op == "bool_lit":
            return "bool"
        else:
            return "unknown"
    elif isinstance(expr, int):
        return "int"
    elif isinstance(expr, float):
        return "double"
    elif isinstance(expr, str):
        return "String"
    return "unknown"

def tipos_compatibles(esperado, actual):
    if esperado == actual:
        return True
    if esperado == "double" and actual == "int":
        return True
    return False

def promover_tipo(t1, t2):
    if "double" in (t1, t2):
        return "double"
    return t1





# Mapeo de archivos a usuarios Git
archivos_usuarios = {
    "algoritmo1.dart": "ljbarzol",
    "algoritmo2.dart": "vic28code",
    "algoritmo3.dart": "AlejandroSV2004"
}

# Crear carpeta de logs si no existe
carpeta_logs = "logsSem"
os.makedirs(carpeta_logs, exist_ok=True)

# Fecha y hora actual para el lote de análisis
fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")

for archivo, usuario in archivos_usuarios.items(): 
    nombre_log = f"semantico-{usuario}-{fecha_hora}.txt"
    ruta_log = os.path.join(carpeta_logs, nombre_log)

    try:
        with open("algoritmos/" + archivo, 'r', encoding='utf-8') as f_in:
            data = f_in.read()

        with open(ruta_log, "w", encoding="utf-8") as log_file:
            with redirect_stdout(log_file):  # Todo lo que se imprima, se guarda en el log
                print(f"--- Análisis Semántico de: {archivo} (Usuario: {usuario}) ---\n")

                lexer.lineno = 1
                arbol_sintactico = parser.parse(data, lexer=lexer)

                if arbol_sintactico:
                    print("\n--- Resultado del Análisis Semántico ---\n")
                    resultado_semantico = analizar(arbol_sintactico)
                    print(resultado_semantico)

                    print("\n--- Tabla de Símbolos ---")
                    print(pformat(symbol_table))
                else:
                    print("Error: No se pudo generar el árbol sintáctico. Análisis semántico no realizado.\n")

    except FileNotFoundError:
        with open(ruta_log, "w", encoding="utf-8") as log_file:
            log_file.write(f"Error: El archivo de entrada '{archivo}' no fue encontrado.\n")
    except Exception as e:
        with open(ruta_log, "w", encoding="utf-8") as log_file:
            log_file.write(f"Ocurrió un error inesperado al procesar {archivo}: {e}\n")


