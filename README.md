# Analizador de Código en Dart

Este proyecto es un **Analizador Léxico, Sintáctico y Semántico para el lenguaje Dart**, implementado en **Python** usando **PLY (Python Lex-Yacc)** y **Tkinter** para la interfaz gráfica.  
Incluye:
- Análisis léxico con generación de tokens.
- Análisis sintáctico con generación de AST.
- Análisis semántico con tabla de símbolos.
- Interfaz gráfica amigable con pestañas y botones para ejecutar cada análisis.
- Logos decorativos de Dart y Python para un toque visual.

---

## ⚙️ Requisitos

### Python

- Python **3.8 o superior**
- Recomendable usar un **entorno virtual**

### Bibliotecas necesarias

Instálalas con:

- pip install ply pillow
- **`ply`**: Para crear el analizador léxico y sintáctico.
- **`pillow (PIL)`**: Para mostrar imágenes en la interfaz Tkinter.

> **Tkinter** ya viene incluido con Python en la mayoría de instalaciones.  
> Si no lo tienes, instálalo según tu sistema operativo.

---

## 📝 Notas

- Los logs por archivo se guardan automáticamente en:
  - `logsLex/`
  - `logsSintax/`
  - `logsSem/`

- La tabla de símbolos se muestra en la salida de cada analizador.
- El OUTPUT está protegido como solo lectura, no editable por el usuario.

---

## 👥 Autores

- Leidy Barzola
- Hilda Angulo
- Alejandro Sornoza
