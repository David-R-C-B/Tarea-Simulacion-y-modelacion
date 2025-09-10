"""
Ventana principal con tema aplicado + barra animada superior.
Incluye importación de módulos que se autoregistran en Registry.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from core.app_state import AppState
from gui.tab_generadores import GeneradoresTab
from gui.tab_pruebas import PruebasTab
from gui.tab_variables import VariablesTab
from gui.theme import apply_theme
from gui.widgets import ScanBar

# -------- Generadores registrados (solo los que quieres) --------
import generators.mid_square               # noqa: F401
import generators.productos_medios         # noqa: F401
import generators.multiplicador_constante  # noqa: F401
# (No importamos generators.numpy_uniform para que no aparezca)

# -------- Pruebas registradas (sin placeholders) --------
import tests.medias                        # noqa: F401
import tests.varianza                      # noqa: F401
import tests.uniformidad_chi2              # noqa: F401

def launch_app() -> None:
    root = tk.Tk()
    root.title("Simulación y Modelación – Pseudoaleatorios")
    root.geometry("1100x750")
    root.minsize(980, 620)

    # Tema
    apply_theme(root)

    # Estado global
    state = AppState()

    # Header con scan bar
    header = ttk.Frame(root, style="Root.TFrame")
    header.pack(fill="x")
    title_row = ttk.Frame(header, style="Header.TFrame")
    title_row.pack(fill="x")
    ttk.Label(title_row, text="Generadores & Pruebas de Pseudoaleatorios", style="Title.TLabel").pack(
        side="left", padx=16, pady=10)
    ttk.Label(title_row, text="Materia: Simulación y Modelación", style="Subtle.TLabel").pack(
        side="right", padx=16)

    ScanBar(root, height=3).pack(fill="x")

    # Menú
    menubar = tk.Menu(root)
    menu_archivo = tk.Menu(menubar, tearoff=0)
    menu_archivo.add_command(label="Acerca de…", command=lambda: messagebox.showinfo(
        "Acerca de",
        "Proyecto de Simulación y Modelación\nGUI de números pseudoaleatorios\nPython 3.10+"
    ))
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", command=root.destroy)
    menubar.add_cascade(label="Archivo", menu=menu_archivo)
    root.config(menu=menubar)

    # Notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    tab_generadores = GeneradoresTab(notebook, state)
    tab_pruebas = PruebasTab(notebook, state)
    tab_variables = VariablesTab(notebook, state)

    notebook.add(tab_generadores, text="Generadores")
    notebook.add(tab_pruebas, text="Pruebas")
    notebook.add(tab_variables, text="Variables")

    notebook.select(0)
    root.mainloop()
