from pprint import pformat
from contextlib import redirect_stdout
from sintactico import parser, lexer
import os
from datetime import datetime
from io import StringIO
from pprint import pformat
# -------------------------
# Tabla de símbolos global
# -------------------------
symbol_table = {}

# -------------------------
# Análisis semántico general
# -------------------------

# -------------------------
# Agregado de cambios varios para
# ajustar el analisis semantico a
# los algoritmos planteados
# - Hilda Angulo
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
        elif tipo == 'final_declaration':   
            manejar_variable(decl, symbol_table, constante=True)

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
    elif tipo == 'final_declaration':
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

    # Permitir redeclaración de variables en bucles for (ámbito local)
    # Solo verificar duplicados para variables globales o de función
    if nombre in tabla and not nombre.startswith('_loop_'):
        # Marcar variables de bucle con un prefijo especial para evitar conflictos
        tabla[f'_loop_{nombre}'] = tipo_esperado
    else:
        tabla[nombre] = tipo_esperado

    if valor is not None:
       tipo_valor = evaluar_expr(valor, tabla)
       if tipo_esperado == 'var':
           tipo_esperado = tipo_valor
           tabla[nombre] = tipo_esperado
       elif not tipos_compatibles(tipo_esperado, tipo_valor):
           raise Exception(f"Tipo incorrecto en '{nombre}': se esperaba {tipo_esperado}, se recibió {tipo_valor}")

    print(f"[OK] {'Constante' if constante else 'Variable'} '{nombre}' declarada como {tipo_esperado}")

def obtener_tipo(tipo):
    if isinstance(tipo, tuple):
        if tipo[0] == 'type':
            return tipo[1]
        elif tipo[0] == 'nullable_type':
            return obtener_tipo(tipo[1]) + '?'
        elif tipo[0] == 'generic':
            tipo_base = tipo[1]
            tipo_param = obtener_tipo(tipo[2][0])
            return f"{tipo_base}<{tipo_param}>"
        elif tipo[0] == 'set':
            elementos = tipo[1]
            tipos_elementos = set()
            for elemento in elementos:
                tipo_elem = obtener_tipo(elemento) if isinstance(elemento, tuple) else evaluar_expr(elemento, {})
                tipos_elementos.add(tipo_elem)
            if len(tipos_elementos) == 1:
                return f"Set<{tipos_elementos.pop()}>"
            else:
                return "Set<dynamic>"
        elif tipo[0] == 'map':
            pares = tipo[1]
            tipos_keys = set()
            tipos_vals = set()
            for clave, valor in pares:
                tipo_k = obtener_tipo(clave) if isinstance(clave, tuple) else evaluar_expr(clave, {})
                tipo_v = obtener_tipo(valor) if isinstance(valor, tuple) else evaluar_expr(valor, {})
                tipos_keys.add(tipo_k)
                tipos_vals.add(tipo_v)
            tipo_k = tipos_keys.pop() if len(tipos_keys) == 1 else "dynamic"
            tipo_v = tipos_vals.pop() if len(tipos_vals) == 1 else "dynamic"
            return f"Map<{tipo_k}, {tipo_v}>"

    elif isinstance(tipo, str):
        return tipo
    elif isinstance(tipo, int):
        return "int"
    elif isinstance(tipo, float):
        return "double"
    elif isinstance(tipo, bool):
        return "bool"
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
                # Buscar también con prefijo de bucle
                nombre_bucle = f'_loop_{nombre}'
                if nombre_bucle in tabla:
                    tipo_simbolo = tabla[nombre_bucle]
                    if isinstance(tipo_simbolo, dict):
                        return tipo_simbolo["tipo"]  # función
                    return tipo_simbolo  # variable
                
                # Manejar variables especiales del sistema
                if nombre == "stdin":
                    return "Stdin"
                elif nombre == "stdout":
                    return "Stdout"
                elif nombre == "stderr":
                    return "Stderr"
                else:
                    raise Exception(f"Variable o función no declarada: {nombre}")
            tipo_simbolo = tabla[nombre]
            if isinstance(tipo_simbolo, dict):
                return tipo_simbolo["tipo"]  # función
            return tipo_simbolo  # variable
        elif op == "ternary":
            condicion = expr[1]
            verdadero = expr[2]
            falso = expr[3]

            tipo_cond = evaluar_expr(condicion, tabla)
            if tipo_cond != "bool":
                raise Exception(f"Condición del ternario debe ser booleana, se recibió {tipo_cond}")

            tipo_v = evaluar_expr(verdadero, tabla)
            tipo_f = evaluar_expr(falso, tabla)

            if tipos_compatibles(tipo_v, tipo_f):
                return tipo_v  # o tipo_f, son iguales
            else:
                return "dynamic"

        elif op == "call":
            funcion = expr[1]
            args = expr[2]
            if isinstance(funcion, tuple) and funcion[0] == "var":
                nombre_funcion = funcion[1]
                # Validar argumentos antes de continuar
                validar_argumentos_funcion(nombre_funcion, args, tabla)
                if nombre_funcion in tabla and isinstance(tabla[nombre_funcion], dict):
                    return tabla[nombre_funcion]["tipo"]
                else:
                    raise Exception(f"Función '{nombre_funcion}' no declarada.")
            elif isinstance(funcion, tuple) and funcion[0] == "member_access":
                # Llamada a método de objeto: objeto.metodo(args)
                objeto = funcion[1]
                metodo = funcion[2]
                tipo_objeto = evaluar_expr(objeto, tabla)
                for arg in args:
                    evaluar_expr(arg, tabla)
                # Manejar métodos conocidos de tipos específicos
                if tipo_objeto == "Stdin" and metodo == "readLineSync":
                    return "String?"
                elif tipo_objeto == "String" and metodo == "parse":
                    return "int"
                elif tipo_objeto == "String" and metodo == "isEmpty":
                    return "bool"
                elif tipo_objeto == "String" and metodo == "isNotEmpty":
                    return "bool"
                elif tipo_objeto.startswith("List<") and metodo == "add":
                    return "void"
                elif tipo_objeto.startswith("List<") and metodo == "remove":
                    return "bool"
                elif tipo_objeto.startswith("List<") and metodo == "clear":
                    return "void"
                else:
                    # Para métodos no reconocidos, devolver dynamic
                    return "dynamic"
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
        elif op == "set":
            elementos = expr[1]
            tipos_elementos = set()
            for elemento in elementos:
                tipos_elementos.add(evaluar_expr(elemento, tabla))
            if len(tipos_elementos) == 1:
                return f"Set<{tipos_elementos.pop()}>"
            else:
                return "Set<dynamic>"

        elif op == "map":
            pares = expr[1]
            tipos_keys = set()
            tipos_vals = set()
            for clave, valor in pares:
                tipos_keys.add(evaluar_expr(clave, tabla))
                tipos_vals.add(evaluar_expr(valor, tabla))
            tipo_k = tipos_keys.pop() if len(tipos_keys) == 1 else "dynamic"
            tipo_v = tipos_vals.pop() if len(tipos_vals) == 1 else "dynamic"
            return f"Map<{tipo_k}, {tipo_v}>"

        elif op in ('+', '-', '*', '/', '//', '%'):
            t1 = evaluar_expr(expr[1], tabla)
            t2 = evaluar_expr(expr[2], tabla)
            return promover_tipo(t1, t2)
        elif op in ('MINSIGNEQ', 'MAXSIGNEQ', 'MINSIGN', 'MAXSIGN', 'EQEQ', 'NEQ', '>=', '<=', '>', '<', '==', '!='):
            # Operadores relacionales siempre devuelven bool
            evaluar_expr(expr[1], tabla)  # Verificar que los operandos existan
            evaluar_expr(expr[2], tabla)
            return "bool"
        elif op in ('AND', 'OR', '&&', '||'):
            # Operadores lógicos siempre devuelven bool
            t1 = evaluar_expr(expr[1], tabla)
            t2 = evaluar_expr(expr[2], tabla)
            if t1 != "bool" or t2 != "bool":
                raise Exception(f"Operadores lógicos requieren operandos booleanos, se recibió {t1} y {t2}")
            return "bool"
        elif op == "not":
            # Operador NOT siempre devuelve bool
            t1 = evaluar_expr(expr[1], tabla)
            if t1 != "bool":
                raise Exception(f"Operador NOT requiere operando booleano, se recibió {t1}")
            return "bool"
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
        elif op == "is":
            # Operador 'is' para verificación de tipo
            return "bool"
        elif op == "is!":
            # Operador 'is!' para verificación de tipo negada
            return "bool"
        else:
            return "unknown"

    elif isinstance(expr, int):
        return "int"
    elif isinstance(expr, float):
        return "double"
    elif isinstance(expr, str):
    # Manejar booleanos que vienen como string
        if expr == "true" or expr == "false":
            return "bool"
    # Validar si el string es realmente un número entero
        try:
            int(expr)
            return "int"
        except ValueError:
            pass
        try:
            float(expr)
            return "double"
        except ValueError:
            pass
    # Si no es número, es cadena
        return "String"


# -------------------------
# Compatibilidad de tipos
# -------------------------
def tipos_compatibles(esperado, actual):
    if esperado == actual:
        return True
    # Promoción válida: int se puede usar donde se espera double
    if esperado == "double" and actual == "int":
        return True
    # Colecciones genéricas compatibles
    if esperado.startswith("List<") and actual.startswith("List<"):
        return True
    if esperado.startswith("Map<") and actual.startswith("Map<"):
        return True
    if esperado.startswith("Set<") and actual.startswith("Set<"):
        return True
    # TODO: Aquí NO permitir int vs String ni bool vs int, etc.
    return False



def promover_tipo(t1, t2):
    if "double" in (t1, t2):
        return "double"
    return t1

def analizar_instruccion(instruccion, tabla_local, tipo_retorno, nombre_funcion):
    """Analiza una instrucción recursivamente, buscando return statements"""
    if isinstance(instruccion, tuple):
        if instruccion[0] == 'return':
            _, expr = instruccion
            tipo_expr = evaluar_expr(expr, tabla_local) if expr else 'void'
            if not tipos_compatibles(tipo_retorno, tipo_expr):
                raise Exception(
                    f"Tipo de retorno inválido en '{nombre_funcion}': se esperaba {tipo_retorno}, se recibió {tipo_expr}")
        elif instruccion[0] == 'if':
            # Analizar instrucción if (puede contener return)
            analizar_instruccion(instruccion[2], tabla_local, tipo_retorno, nombre_funcion)
        elif instruccion[0] == 'if_else':
            # Analizar instrucciones if-else (pueden contener return)
            analizar_instruccion(instruccion[2], tabla_local, tipo_retorno, nombre_funcion)
            analizar_instruccion(instruccion[3], tabla_local, tipo_retorno, nombre_funcion)
        elif instruccion[0] == 'block':
            # Analizar bloque de instrucciones
            for instr in instruccion[1]:
                analizar_instruccion(instr, tabla_local, tipo_retorno, nombre_funcion)
        elif instruccion[0] == '=':
            # Asignación directa
            evaluar_expr(instruccion, tabla_local)
        elif instruccion[0] == 'expression':
            evaluar_expr(instruccion[1], tabla_local)

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
            elif instruccion[0] == 'for':
                # Registrar variables declaradas en bucles for
                _, inicializacion, _, _, _ = instruccion
                if isinstance(inicializacion, tuple) and inicializacion[0] == 'variable_declaration':
                    manejar_variable(inicializacion, tabla_local)
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
            elif instruccion[0] == 'if':
                # Analizar instrucción if (puede contener return)
                analizar_instruccion(instruccion[2], tabla_local, tipo_retorno, nombre)
            elif instruccion[0] == 'if_else':
                # Analizar instrucciones if-else (pueden contener return)
                analizar_instruccion(instruccion[2], tabla_local, tipo_retorno, nombre)
                analizar_instruccion(instruccion[3], tabla_local, tipo_retorno, nombre)
            else:
                # Analizar estructuras de control con contexto de función
                analizar_estructuras_control(instruccion, tabla_local, 'function')
            # Las declaraciones ya fueron manejadas en la primera pasada
    print(f"[OK] Función '{nombre}' analizada correctamente con tipo de retorno '{tipo_retorno}'")


# -------------------------
# Estructuras de control
# Número correcto de argumentos en funciones
# Hilda Angulo
# -------------------------

def validar_argumentos_funcion(nombre_funcion, args_provistos, tabla):
    """Valida número y tipo de argumentos en llamadas a funciones"""
    if nombre_funcion not in tabla or not isinstance(tabla[nombre_funcion], dict):
        raise Exception(f"Función '{nombre_funcion}' no declarada.")
    
    funcion_info = tabla[nombre_funcion]
    parametros_esperados = funcion_info['parametros']
    
    if len(args_provistos) != len(parametros_esperados):
        raise Exception(f"Función '{nombre_funcion}' espera {len(parametros_esperados)} argumentos, se proporcionaron {len(args_provistos)}")
    
    for i, (arg_provisto, (tipo_esperado, nombre_param)) in enumerate(zip(args_provistos, parametros_esperados)):
        tipo_provisto = evaluar_expr(arg_provisto, tabla)
        tipo_esperado_obtenido = obtener_tipo(tipo_esperado)
        
        if not tipos_compatibles(tipo_esperado_obtenido, tipo_provisto):
            raise Exception(f"Argumento {i+1} de '{nombre_funcion}': se esperaba {tipo_esperado_obtenido}, se recibió {tipo_provisto}")
    
    print(f"[OK] Llamada a función '{nombre_funcion}' con argumentos válidos")

def analizar_estructuras_control(instruccion, tabla_local, contexto_actual="global"):
    """Analiza estructuras de control y valida break, continue, return"""
    if not isinstance(instruccion, tuple):
        return
    
    tipo_instruccion = instruccion[0]
    
    if tipo_instruccion == 'break':
        if contexto_actual not in ['for', 'while', 'do_while']:
            raise Exception("'break' solo puede usarse dentro de bucles")
        print("[OK] 'break' usado correctamente dentro de bucle")
        
    elif tipo_instruccion == 'continue':
        if contexto_actual not in ['for', 'while', 'do_while']:
            raise Exception("'continue' solo puede usarse dentro de bucles")
        print("[OK] 'continue' usado correctamente dentro de bucle")
        
    elif tipo_instruccion == 'return':
        if contexto_actual != 'function':
            raise Exception("'return' solo puede usarse dentro de funciones")
        print("[OK] 'return' usado correctamente dentro de función")
        
    elif tipo_instruccion == 'for':
        _, inicializacion, condicion, incremento, cuerpo = instruccion
        
        # Registrar variables declaradas en la inicialización del bucle for
        if isinstance(inicializacion, tuple) and inicializacion[0] == 'variable_declaration':
            manejar_variable(inicializacion, tabla_local)
        elif isinstance(inicializacion, tuple) and inicializacion[0] == '=':
            # Para asignaciones como i = 0
            evaluar_expr(inicializacion, tabla_local)
        
        if condicion:
            tipo_condicion = evaluar_expr(condicion, tabla_local)
            if tipo_condicion != "bool":
                raise Exception(f"Condición de bucle 'for' debe ser booleana, se recibió {tipo_condicion}")
        
        analizar_cuerpo_control(cuerpo, tabla_local, 'for')
        
    elif tipo_instruccion == 'while':
        _, condicion, cuerpo = instruccion
        tipo_condicion = evaluar_expr(condicion, tabla_local)
        if tipo_condicion != "bool":
            raise Exception(f"Condición de bucle 'while' debe ser booleana, se recibió {tipo_condicion}")
        analizar_cuerpo_control(cuerpo, tabla_local, 'while')
        
    elif tipo_instruccion == 'if':
        _, condicion, cuerpo = instruccion
        tipo_condicion = evaluar_expr(condicion, tabla_local)
        if tipo_condicion != "bool":
            raise Exception(f"Condición de 'if' debe ser booleana, se recibió {tipo_condicion}")
        analizar_cuerpo_control(cuerpo, tabla_local, contexto_actual)
        
    elif tipo_instruccion == 'if_else':
        _, condicion, cuerpo_if, cuerpo_else = instruccion
        tipo_condicion = evaluar_expr(condicion, tabla_local)
        if tipo_condicion != "bool":
            raise Exception(f"Condición de 'if-else' debe ser booleana, se recibió {tipo_condicion}")
        analizar_cuerpo_control(cuerpo_if, tabla_local, contexto_actual)
        analizar_cuerpo_control(cuerpo_else, tabla_local, contexto_actual)

def analizar_cuerpo_control(cuerpo, tabla_local, contexto):
    """Analiza el cuerpo de una estructura de control"""
    if isinstance(cuerpo, list):
        for instruccion in cuerpo:
            analizar_estructuras_control(instruccion, tabla_local, contexto)
    elif isinstance(cuerpo, tuple):
        analizar_estructuras_control(cuerpo, tabla_local, contexto)

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

# -------------------------
# ANALIZADOR SEMÁNTICO PARA LA INTERFAZ
# -------------------------

from pprint import pformat

def analizar_semantico(codigo):
    from sintactico import parser, lexer
    from contextlib import redirect_stdout

    symbol_table = {}
    lexer.lineno = 1
    buffer = StringIO()  # Captura todo lo que se imprime

    try:
        ast = parser.parse(codigo, lexer=lexer)
        if not ast:
            return ["Error: No se pudo generar AST. Revisa tu entrada."]
        
        with redirect_stdout(buffer):
            analizar(ast, symbol_table)
        
        salida_ok = buffer.getvalue()
        resultado = ["--- Resultado del Análisis Semántico ---", salida_ok.strip(), "--- Tabla de Símbolos ---", pformat(symbol_table)]
        return resultado
    except Exception as e:
        return [f"Error semántico: {e}"]