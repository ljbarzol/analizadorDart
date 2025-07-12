import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from lexico import analizar_lexico
from sintactico import analizar_sintactico
from semantico import analizar_semantico

# --- Ventana principal ---
root = tk.Tk()
root.title("✨ ANALIZADOR DE CÓDIGO EN DART ✨")
root.geometry("900x600")
root.configure(bg="#2C2F33")

# --- Colores base ---
BG_MAIN = "#2C2F33"
BG_PANEL = "#23272A"
FG_TEXT = "#FFFFFF"
COLOR_BUTTON = "#7289DA"
COLOR_OUTPUT = "#99AAB5"

from PIL import Image, ImageTk

# --- Título superior ---
# Cargar y redimensionar logos
img_dart = Image.open("logo_dart.png").resize((40, 40))
logo_dart = ImageTk.PhotoImage(img_dart)

img_python = Image.open("logo_python.png").resize((40, 40))
logo_python = ImageTk.PhotoImage(img_python)

frame_titulo = tk.Frame(root, bg=COLOR_BUTTON, height=50)
frame_titulo.pack(fill=tk.X)

# Logo Dart a la izquierda
lbl_logo_dart = tk.Label(frame_titulo, image=logo_dart, bg=COLOR_BUTTON)
lbl_logo_dart.pack(side=tk.LEFT, padx=10)

# Título centrado
lbl_titulo = tk.Label(frame_titulo, text="ANALIZADOR DE CÓDIGO EN DART", bg=COLOR_BUTTON,
                      fg=FG_TEXT, font=("Arial", 16, "bold"))
lbl_titulo.pack(side=tk.LEFT, expand=True)

# Logo Python a la derecha
lbl_logo_python = tk.Label(frame_titulo, image=logo_python, bg=COLOR_BUTTON)
lbl_logo_python.pack(side=tk.RIGHT, padx=10)

# --- Contenedor principal ---
frame_main = tk.Frame(root, bg=BG_MAIN)
frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- Panel de código a la izquierda ---
frame_left = tk.Frame(frame_main, bg=BG_PANEL)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

# Botones de análisis
frame_buttons = tk.Frame(frame_left, bg=BG_PANEL)
frame_buttons.pack(fill=tk.X, pady=5)

def run_lexico():
    text_output.config(state="normal")
    limpiar_output()
    resultado = analizar_lexico(text_codigo.get("1.0", tk.END).strip())
    text_output.insert(tk.END, "\n".join(resultado))
    text_output.config(state="disabled")

def run_sintactico():
    text_output.config(state="normal")
    limpiar_output()
    resultado = analizar_sintactico(text_codigo.get("1.0", tk.END).strip())
    text_output.insert(tk.END, "\n".join(resultado))
    text_output.config(state="disabled")


def run_semantico():
    text_output.config(state="normal")
    limpiar_output()
    resultado = analizar_semantico(text_codigo.get("1.0", tk.END).strip())
    text_output.insert(tk.END, "\n".join(resultado))
    text_output.config(state="disabled")

def run_todo():
    text_output.config(state="normal")
    limpiar_output()
    codigo = text_codigo.get("1.0", tk.END).strip()
    
    text_output.insert(tk.END, "=============================== LÉXICO ================================\n")
    text_output.insert(tk.END, "\n".join(analizar_lexico(codigo)) + "\n\n")
    
    text_output.insert(tk.END, "============================== SINTÁCTICO ==============================\n")
    text_output.insert(tk.END, "\n".join(analizar_sintactico(codigo)) + "\n\n")
    
    text_output.insert(tk.END, "============================== SEMÁNTICO ==============================\n")
    text_output.insert(tk.END, "\n".join(analizar_semantico(codigo)) + "\n\n")
    text_output.config(state="disabled")


def limpiar_output():
    text_output.delete("1.0", tk.END)
    
def limpiar_codigo():
    text_codigo.delete("1.0", tk.END)


btn_lexico = tk.Button(frame_buttons, text="ANALIZADOR LÉXICO", bg=COLOR_BUTTON, fg=FG_TEXT,
                       command=run_lexico, width=20)
btn_lexico.pack(side=tk.LEFT, padx=2)

btn_sintactico = tk.Button(frame_buttons, text="ANALIZADOR SINTÁCTICO", bg=COLOR_BUTTON, fg=FG_TEXT,
                           command=run_sintactico, width=20)
btn_sintactico.pack(side=tk.LEFT, padx=2)

btn_semantico = tk.Button(frame_buttons, text="ANALIZADOR SEMÁNTICO", bg=COLOR_BUTTON, fg=FG_TEXT,
                          command=run_semantico, width=20)
btn_semantico.pack(side=tk.LEFT, padx=2)

btn_todo = tk.Button(frame_buttons, text="ANALIZAR TODO", bg="#43B581", fg=FG_TEXT,
                     command=run_todo, width=20)
btn_todo.pack(side=tk.LEFT, padx=2)

btn_limpiar = tk.Button(
    frame_buttons,
    text="🧹 LIMPIAR",
    bg="#FF5555",
    fg=FG_TEXT,
    command=limpiar_codigo,
    width=15
)
btn_limpiar.pack(side=tk.RIGHT, padx=2)


# TextArea para código
text_codigo = tk.Text(frame_left, bg="#2C2F33", fg=FG_TEXT, insertbackground=FG_TEXT,
                      font=("Consolas", 12))
text_codigo.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

# --- Panel OUTPUT a la derecha ---
frame_right = tk.Frame(frame_main, bg=BG_PANEL, width=300)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH)

lbl_output = tk.Label(frame_right, text="OUTPUT", bg=COLOR_BUTTON, fg=FG_TEXT,
                      font=("Arial", 14, "bold"))
lbl_output.pack(fill=tk.X)

text_output = tk.Text(frame_right, bg="#23272A", fg=FG_TEXT, insertbackground=FG_TEXT,
                      font=("Consolas", 11))

text_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

root.mainloop()
