from pprint import pformat
from contextlib import redirect_stdout
from sintactico import parser, lexer
import os
from datetime import datetime

# -------------------------
# Tabla de símbolos global
# -------------------------
symbol_table = {}

# -------------------------
# Análisis semántico general
# -------------------------
def analizar(ast):
    if not ast or ast[0] != 'program':
        raise Exception("AST inválido o vacío")
    
    declaraciones = ast[1]
    for decl in declaraciones:
        analizar_declaracion(decl)
    return symbol_table

def analizar_declaracion(node):
    tipo = node[0]

    if tipo == 'variable_declaration':
        manejar_variable(node)
    elif tipo == 'const_declaration':
        manejar_variable(node, constante=True)
    elif tipo == 'function':
        analizar_funcion(node)

# -------------------------
# Variables y Constantes
# Leidy Barzola
# -------------------------
def manejar_variable(node, constante=False):
    _, tipo_decl, nombre, valor = node

    # Reconocer listas genéricas
    if isinstance(tipo_decl, tuple) and tipo_decl[0] == 'generic':
        tipo_base = tipo_decl[1]
        tipo_param = obtener_tipo(tipo_decl[2][0])
        tipo_esperado = f"{tipo_base}<{tipo_param}>"
    else:
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

# -------------------------
# Evaluar expresiones
# Incluye asignación y subscript
# -------------------------
def evaluar_expr(expr):
    if isinstance(expr, list) and len(expr) == 1:
        expr = expr[0]

    if isinstance(expr, tuple):
        op = expr[0]

        if op == "var":
            nombre = expr[1]
            if nombre not in symbol_table:
                raise Exception(f"Variable no declarada: {nombre}")
            return symbol_table[nombre]

        elif op == "subscript":
            lista = expr[1]
            valor = expr[2]
            tipo_lista = evaluar_expr(lista)
            tipo_elemento = evaluar_expr(valor)

            if tipo_lista.startswith("List<"):
                tipo_param = tipo_lista[5:-1]
                if not tipos_compatibles("int", tipo_elemento) and not tipos_compatibles("String", tipo_elemento):
                    raise Exception(
                        f"Tipo de índice inválido: se esperaba int, se recibió {tipo_elemento}")
                return tipo_param
            else:
                raise Exception(f"No se puede indexar tipo '{tipo_lista}'")

        elif op == "=":
            izquierda = expr[1]
            derecha = expr[2]

            tipo_izquierda = evaluar_expr(izquierda)
            tipo_derecha = evaluar_expr(derecha)

            if not tipos_compatibles(tipo_izquierda, tipo_derecha):
                raise Exception(
                    f"Tipo incompatible en asignación: se esperaba {tipo_izquierda}, se recibió {tipo_derecha}")
            return tipo_izquierda

        elif op == "array":
            elementos = expr[1]
            tipo_elementos = set()
            for elemento in elementos:
                tipo_elementos.add(evaluar_expr(elemento))
            if len(tipo_elementos) == 1:
                return f"List<{tipo_elementos.pop()}>"
            else:
                return "List<dynamic>"

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

# -------------------------
# Compatibilidad de tipos
# -------------------------
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

# -------------------------
# Funciones
# Alejandro Sornoza
# -------------------------
def analizar_funcion(node):
    _, tipo_retorno, nombre, parametros, body = node
    tipo_retorno = obtener_tipo(tipo_retorno)
    symbol_table[nombre] = {'tipo': tipo_retorno, 'parametros': parametros}

    for instruccion in body:
        if isinstance(instruccion, tuple):
            if instruccion[0] == 'return':
                _, expr = instruccion
                tipo_expr = evaluar_expr(expr) if expr else 'void'
                if not tipos_compatibles(tipo_retorno, tipo_expr):
                    raise Exception(
                        f"Tipo de retorno inválido en '{nombre}': se esperaba {tipo_retorno}, se recibió {tipo_expr}")

            elif instruccion[0] == '=':
                # Asignación directa
                evaluar_expr(instruccion)

            elif instruccion[0] == 'expression':
                evaluar_expr(instruccion[1])

            elif instruccion[0] == 'variable_declaration':
                manejar_variable(instruccion)

    print(f"[OK] Función '{nombre}' analizada correctamente con tipo de retorno '{tipo_retorno}'")


# -------------------------
# Logs por archivo
# -------------------------
archivos_usuarios = {
    "algoritmo1.dart": "ljbarzol",
    "algoritmo2.dart": "vic28code",
    "algoritmo3.dart": "AlejandroSV2004"
}

carpeta_logs = "logsSem"
os.makedirs(carpeta_logs, exist_ok=True)

fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")

for archivo, usuario in archivos_usuarios.items():
    numero_algoritmo = archivo.replace("algoritmo", "").replace(".dart", "")
    nombre_log = f"semantico-{usuario}-algoritmo{numero_algoritmo}-{fecha_hora}.txt"
    ruta_log = os.path.join(carpeta_logs, nombre_log)

    try:
        with open("algoritmos/" + archivo, 'r', encoding='utf-8') as f_in:
            data = f_in.read()

        with open(ruta_log, "w", encoding="utf-8") as log_file:
            with redirect_stdout(log_file):
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

    print(f"Log generado: {ruta_log}")
