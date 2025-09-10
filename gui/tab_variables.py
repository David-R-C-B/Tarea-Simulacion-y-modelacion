"""
Tab 'Variables':
- Parámetros globales: k (histograma y m en χ² uniformidad) y α (significancia).
"""
import tkinter as tk
from tkinter import ttk, messagebox
from core.app_state import AppState
from gui.widgets import HoverAccentButton, Toast

class VariablesTab(ttk.Frame):
    def __init__(self, parent, state: AppState):
        super().__init__(parent)
        self.state = state

        frame = ttk.Labelframe(self, text="Parámetros de pruebas y gráficos")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="k (bins / m en χ²):").grid(row=0, column=0, padx=8, pady=10, sticky="e")
        self.entry_k = ttk.Entry(frame, width=12)
        self.entry_k.insert(0, str(self.state.params["k"]))
        self.entry_k.grid(row=0, column=1, padx=6, pady=10, sticky="w")

        ttk.Label(frame, text="α (significancia):").grid(row=0, column=2, padx=8, pady=10, sticky="e")
        self.entry_alpha = ttk.Entry(frame, width=12)
        self.entry_alpha.insert(0, str(self.state.params["alpha"]))
        self.entry_alpha.grid(row=0, column=3, padx=6, pady=10, sticky="w")

        self.btn_save = HoverAccentButton(frame, text="Guardar", command=self.on_save)
        self.btn_save.grid(row=0, column=4, padx=10, pady=10)

        for i in range(5):
            frame.grid_columnconfigure(i, weight=0)

    def on_save(self) -> None:
        try:
            k = int(self.entry_k.get())
            if k <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("k inválido", "k debe ser un entero positivo.")
            return
        try:
            alpha = float(self.entry_alpha.get())
            if not (0 < alpha < 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("α inválido", "α debe ser un número entre 0 y 1.")
            return

        self.state.params["k"] = k
        self.state.params["alpha"] = alpha
        Toast(self, text="Parámetros guardados ⚙")
