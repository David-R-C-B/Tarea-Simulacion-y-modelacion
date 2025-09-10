"""
Tab 'Pruebas' con estilos oscuros y resultados en fuente monoespaciada.
- Muestra lista de pruebas (Registry).
- Ejecuta y presenta resultados en JSON legible.
- Si alguna prueba devuelve 'warnings', se alerta con messagebox.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List
import json
import numpy as np

from core.app_state import AppState
from core.registry import Registry
from tests.base import RandomnessTest
from gui.widgets import HoverAccentButton, Toast

class PruebasTab(ttk.Frame):
    def __init__(self, parent, state: AppState):
        super().__init__(parent)
        self.state = state

        top = ttk.Labelframe(self, text="Pruebas disponibles")
        top.pack(side="top", fill="x", padx=10, pady=10)

        self.tests_vars: Dict[str, tk.BooleanVar] = {}
        for name in Registry.tests.keys():
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(top, text=name, variable=var).pack(side="left", padx=8, pady=8)
            self.tests_vars[name] = var

        self.btn_run = HoverAccentButton(top, text="Probar", command=self.on_run_tests)
        self.btn_run.pack(side="left", padx=10)

        # Resultados
        bottom = ttk.Labelframe(self, text="Resultados")
        bottom.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.txt_results = tk.Text(bottom, height=20, bg="#0F141E", fg="#E6EAF2",
                                   insertbackground="#E6EAF2", font=("Consolas", 10))
        self.txt_results.pack(fill="both", expand=True)

    def on_run_tests(self) -> None:
        if self.state.sequence is None:
            messagebox.showwarning("Pruebas", "Primero genera una secuencia.")
            return

        selected = [name for name, var in self.tests_vars.items() if var.get()]
        if not selected:
            messagebox.showinfo("Pruebas", "Selecciona al menos una prueba.")
            return

        self.txt_results.delete("1.0", "end")
        results_summary: List[Dict[str, Any]] = []

        # Variables globales
        alpha = self.state.params.get("alpha", 0.05)
        k_bins = self.state.params.get("k", 10)  # usaremos k como m en uniformidad

        for name in selected:
            factory = Registry.tests.get(name)
            if factory is None:
                continue
            test_obj: RandomnessTest = factory()
            res: Dict[str, Any] = test_obj.run(
                self.state.sequence,
                alpha=alpha,
                # pasamos ambos por si alguna prueba usa k o m
                k=k_bins,
                m=k_bins,
            )
            results_summary.append(res)

        # Mostrar resultados
        self.txt_results.insert("1.0", json.dumps(results_summary, indent=2, ensure_ascii=False))
        Toast(self, text="Pruebas ejecutadas 🧪")

        # Si hay advertencias, mostrarlas
        warnings_all = []
        for r in results_summary:
            if isinstance(r, dict) and r.get("warnings"):
                warnings_all.extend(r["warnings"])
        if warnings_all:
            messagebox.showwarning("Advertencias", "\n".join(dict.fromkeys(warnings_all)))  # unique lines
