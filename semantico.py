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
def analizar(ast, symbol_table):
    if not ast or ast[0] != 'program':
        raise Exception("AST inválido o vacío")

    declaraciones = ast[1]

    # Primera pasada: registrar funciones y variables globales
    for decl in declaraciones:
        tipo = decl[0]
        if tipo == 'function':
            _, tipo_retorno, nombre, parametros, _ = decl
            tipo_retorno = obtener_tipo(tipo_retorno)
            if nombre in symbol_table:
                raise Exception(f"Función '{nombre}' ya declarada.")
            symbol_table[nombre] = {'tipo': tipo_retorno, 'parametros': parametros}
        elif tipo == 'variable_declaration':
            manejar_variable(decl, symbol_table)
        elif tipo == 'const_declaration':
            manejar_variable(decl, symbol_table, constante=True)
        # Puedes extender aquí para clases, imports, etc.

    # Segunda pasada: analizar cuerpos de funciones y expresiones globales
    for decl in declaraciones:
        analizar_declaracion(decl, symbol_table)

    return symbol_table


def analizar_declaracion(node, tabla):
    tipo = node[0]

    if tipo == 'variable_declaration':
        # Ya manejada en la pasada 1
        pass
    elif tipo == 'const_declaration':
        pass
    elif tipo == 'function':
        analizar_funcion(node, tabla)
    elif tipo == 'print':
        evaluar_expr(node[1], tabla)

# -------------------------
# Variables y Constantes
# Leidy Barzola
# -------------------------
def manejar_variable(node, tabla, constante=False):
    _, tipo_decl, nombre, valor = node

    # Reconocer listas genéricas
    if isinstance(tipo_decl, tuple) and tipo_decl[0] == 'generic':
        tipo_base = tipo_decl[1]
        tipo_param = obtener_tipo(tipo_decl[2][0])
        tipo_esperado = f"{tipo_base}<{tipo_param}>"
    else:
        tipo_esperado = obtener_tipo(tipo_decl)

    if nombre in tabla:
        raise Exception(f"Variable '{nombre}' ya está declarada.")

    if valor is not None:
        tipo_valor = evaluar_expr(valor, tabla)
        if not tipos_compatibles(tipo_esperado, tipo_valor):
            raise Exception(f"Tipo incorrecto en '{nombre}': se esperaba {tipo_esperado}, se recibió {tipo_valor}")

    tabla[nombre] = tipo_esperado
    print(f"[OK] {'Constante' if constante else 'Variable'} '{nombre}' declarada como {tipo_esperado}")

def obtener_tipo(tipo):
    if isinstance(tipo, tuple):
        if tipo[0] == 'type':
            return tipo[1]
        elif tipo[0] == 'nullable_type':
            return obtener_tipo(tipo[1]) + '?'
        elif tipo[0] == 'generic':
            # Manejar tipos genéricos como List<int>
            tipo_base = tipo[1]
            tipo_param = obtener_tipo(tipo[2][0])
            return f"{tipo_base}<{tipo_param}>"
    elif isinstance(tipo, str):
        return tipo
    return "unknown"

# -------------------------
# Evaluar expresiones
# Incluye asignación y subscript
def evaluar_expr(expr, tabla):
    if isinstance(expr, list) and len(expr) == 1:
        expr = expr[0]

    if isinstance(expr, tuple):
        op = expr[0]

        if op == "var":
            nombre = expr[1]
            if nombre not in tabla:
                raise Exception(f"Variable o función no declarada: {nombre}")
            tipo_simbolo = tabla[nombre]
            if isinstance(tipo_simbolo, dict):
                return tipo_simbolo["tipo"]  # función
            return tipo_simbolo  # variable

        elif op == "call":
            funcion = expr[1]
            args = expr[2]
            if isinstance(funcion, tuple) and funcion[0] == "var":
                nombre_funcion = funcion[1]
                if nombre_funcion in tabla and isinstance(tabla[nombre_funcion], dict):
                    # Verificar número de parámetros si quieres
                    return tabla[nombre_funcion]["tipo"]
                else:
                    raise Exception(f"Función '{nombre_funcion}' no declarada.")
            else:
                raise Exception(f"Llamada inválida: {funcion}")

        elif op == "subscript":
            lista = expr[1]
            valor = expr[2]
            tipo_lista = evaluar_expr(lista, tabla)
            tipo_elemento = evaluar_expr(valor, tabla)

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

            tipo_izquierda = evaluar_expr(izquierda, tabla)
            tipo_derecha = evaluar_expr(derecha, tabla)

            if not tipos_compatibles(tipo_izquierda, tipo_derecha):
                raise Exception(
                    f"Tipo incompatible en asignación: se esperaba {tipo_izquierda}, se recibió {tipo_derecha}")
            return tipo_izquierda

        elif op == "array":
            elementos = expr[1]
            tipo_elementos = set()
            for elemento in elementos:
                tipo_elementos.add(evaluar_expr(elemento, tabla))
            if len(tipo_elementos) == 1:
                return f"List<{tipo_elementos.pop()}>"
            else:
                return "List<dynamic>"

        elif op in ('+', '-', '*', '/', '//'):
            t1 = evaluar_expr(expr[1], tabla)
            t2 = evaluar_expr(expr[2], tabla)
            return promover_tipo(t1, t2)

        elif op in ("string_lit", "str"):
            return "String"
        elif op == "int_lit":
            return "int"
        elif op == "double_lit":
            return "double"
        elif op == "bool_lit":
            return "bool"
        elif op == "uminus":
            tipo = evaluar_expr(expr[1], tabla)
            if tipo in ("int", "double"):
                return tipo
            else:
                return "unknown"
        elif op == "~/":
            t1 = evaluar_expr(expr[1], tabla)
            t2 = evaluar_expr(expr[2], tabla)
            # División entera: si ambos son int, resultado int; si alguno es double, resultado double
            if t1 == "double" or t2 == "double":
                return "double"
            return "int"
        elif op == "member_access":
            objeto = expr[1]
            propiedad = expr[2]
            tipo_objeto = evaluar_expr(objeto, tabla)
            
            # Manejar propiedades conocidas de tipos específicos
            if tipo_objeto.startswith("List<"):
                if propiedad == "length":
                    return "int"
                elif propiedad == "isEmpty":
                    return "bool"
                elif propiedad == "isNotEmpty":
                    return "bool"
            elif tipo_objeto == "String":
                if propiedad == "length":
                    return "int"
                elif propiedad == "isEmpty":
                    return "bool"
            elif tipo_objeto == "Map":
                if propiedad == "length":
                    return "int"
                elif propiedad == "isEmpty":
                    return "bool"
            
            # Para propiedades no reconocidas, devolver dynamic
            return "dynamic"
        else:
            return "unknown"

    elif isinstance(expr, int):
        return "int"
    elif isinstance(expr, float):
        return "double"
    elif isinstance(expr, str):
        return "String"
    # Si es un valor negativo representado como un número (por ejemplo, -1)
    try:
        if isinstance(expr, (int, float)):
            return "int" if isinstance(expr, int) else "double"
    except Exception:
        pass
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
def analizar_funcion(node, tabla_global):
    _, tipo_retorno, nombre, parametros, body = node
    tipo_retorno = obtener_tipo(tipo_retorno)
    # Registrar la función en la tabla global
    tabla_global[nombre] = {'tipo': tipo_retorno, 'parametros': parametros}
    # Crear tabla local para variables de la función
    tabla_local = dict(tabla_global)  # Hereda funciones y globales, pero variables locales se agregan aquí
    
    # Registrar parámetros de la función en la tabla local
    for tipo_param, nombre_param in parametros:
        tipo_param_obtenido = obtener_tipo(tipo_param)
        tabla_local[nombre_param] = tipo_param_obtenido
        print(f"[OK] Parámetro '{nombre_param}' registrado como {tipo_param_obtenido}")
    
    # Primera pasada: registrar variables locales y constantes
    for instruccion in body:
        if isinstance(instruccion, tuple):
            if instruccion[0] == 'variable_declaration':
                manejar_variable(instruccion, tabla_local)
            elif instruccion[0] == 'const_declaration':
                manejar_variable(instruccion, tabla_local, constante=True)
    # Segunda pasada: analizar instrucciones
    for instruccion in body:
        if isinstance(instruccion, tuple):
            if instruccion[0] == 'return':
                _, expr = instruccion
                tipo_expr = evaluar_expr(expr, tabla_local) if expr else 'void'
                if not tipos_compatibles(tipo_retorno, tipo_expr):
                    raise Exception(
                        f"Tipo de retorno inválido en '{nombre}': se esperaba {tipo_retorno}, se recibió {tipo_expr}")
            elif instruccion[0] == '=':
                # Asignación directa
                evaluar_expr(instruccion, tabla_local)
            elif instruccion[0] == 'expression':
                evaluar_expr(instruccion[1], tabla_local)
            # Las declaraciones ya fueron manejadas en la primera pasada
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

    # Crear tabla de símbolos independiente para cada archivo
    symbol_table = {}

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
                    resultado_semantico = analizar(arbol_sintactico, symbol_table)
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
