"""
Tab 'Generadores' con look oscuro, métricas tipo 'chips', botones con hover
y tostadas de confirmación. La tabla muestra los *pasos* cuando el generador
provee `trace`. Ahora soporta algoritmos que requieren **dos semillas**
y/o **constante 'a'**.
"""
from typing import Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np

from core.app_state import AppState
from core.registry import Registry
from utils.exporter import export_sequence_to_csv
from utils.plotting import draw_histogram
from gui.widgets import HoverAccentButton, Toast
from gui.theme import PALETTE

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GeneradoresTab(ttk.Frame):
    def __init__(self, parent, state: AppState):
        super().__init__(parent)
        self.state = state

        # --- Panel Controles ---
        controls = ttk.Labelframe(self, text="Controles")
        controls.pack(side="top", fill="x", padx=10, pady=10)

        ttk.Label(controls, text="Algoritmo:").grid(row=0, column=0, padx=6, pady=8, sticky="e")
        self.combo_alg = ttk.Combobox(controls, state="readonly", width=38,
                                      values=list(Registry.generators.keys()))
        if self.combo_alg["values"]:
            self.combo_alg.current(0)
        self.combo_alg.grid(row=0, column=1, padx=6, pady=8, sticky="w")
        self.combo_alg.bind("<<ComboboxSelected>>", self._on_algorithm_changed)

        ttk.Label(controls, text="n:").grid(row=0, column=2, padx=6, pady=8, sticky="e")
        self.entry_n = ttk.Entry(controls, width=10)
        self.entry_n.insert(0, str(self.state.params["n"]))
        self.entry_n.grid(row=0, column=3, padx=6, pady=8, sticky="w")

        # Semillas y constante (dinámicos según algoritmo)
        self.lbl_seed1 = ttk.Label(controls, text="Semilla 1:")
        self.lbl_seed1.grid(row=0, column=4, padx=6, pady=8, sticky="e")
        self.entry_seed1 = ttk.Entry(controls, width=14)
        self.entry_seed1.insert(0, "" if self.state.params["seed"] is None else str(self.state.params["seed"]))
        self.entry_seed1.grid(row=0, column=5, padx=6, pady=8, sticky="w")

        self.lbl_seed2 = ttk.Label(controls, text="Semilla 2:")
        self.entry_seed2 = ttk.Entry(controls, width=14)
        self.lbl_seed2.grid_forget()
        self.entry_seed2.grid_forget()

        self.lbl_const = ttk.Label(controls, text="Constante (a):")
        self.entry_const = ttk.Entry(controls, width=14)
        self.lbl_const.grid_forget()
        self.entry_const.grid_forget()

        self.btn_generar = HoverAccentButton(controls, text="Generar", command=self.on_generate)
        self.btn_generar.grid(row=0, column=12, padx=10, pady=8)

        self.btn_export_csv = ttk.Button(controls, text="Exportar CSV", command=self.on_export_csv)
        self.btn_export_csv.grid(row=0, column=13, padx=6, pady=8)

        self.btn_save_png = ttk.Button(controls, text="Guardar PNG", command=self.on_save_png)
        self.btn_save_png.grid(row=0, column=14, padx=6, pady=8)

        # Distribución columnas
        for i in range(15):
            controls.grid_columnconfigure(i, weight=0)
        controls.grid_columnconfigure(1, weight=1)

        # --- Panel central split ---
        middle = ttk.Panedwindow(self, orient="horizontal")
        middle.pack(fill="both", expand=True, padx=10, pady=5)

        # Izquierda: tabla + métricas
        left_frame = ttk.Frame(middle)
        middle.add(left_frame, weight=1)

        metrics = ttk.Frame(left_frame)
        metrics.pack(fill="x", padx=2, pady=(0, 6))
        self.lbl_n = ttk.Label(metrics, text="n: —", style="Metric.TLabel")
        self.lbl_mu = ttk.Label(metrics, text="μ: —", style="Metric.TLabel")
        self.lbl_sd = ttk.Label(metrics, text="σ: —", style="Metric.TLabel")
        self.lbl_min = ttk.Label(metrics, text="min: —", style="Metric.TLabel")
        self.lbl_max = ttk.Label(metrics, text="max: —", style="Metric.TLabel")
        for w in (self.lbl_n, self.lbl_mu, self.lbl_sd, self.lbl_min, self.lbl_max):
            w.pack(side="left", padx=6, pady=4)

        self.tree = ttk.Treeview(left_frame, columns=("index", "value"), show="headings", height=22)
        self.tree.heading("index", text="Índice")
        self.tree.heading("value", text="Valor / Paso")
        self.tree.column("index", width=80, anchor="e")
        self.tree.column("value", width=780, anchor="w")
        self.tree.pack(fill="both", expand=True)

        # Derecha: gráfico
        right_frame = ttk.Frame(middle)
        middle.add(right_frame, weight=1)

        self.figure = Figure(figsize=(5, 4), dpi=100, facecolor=PALETTE["elev"])
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Inicializar visibilidad dinámica
        self._on_algorithm_changed()

    # ----------------- Handlers -----------------

    def _parse_int_or_none(self, s: str) -> Optional[int]:
        s = s.strip()
        if not s:
            return None
        try:
            return int(s)
        except ValueError:
            return None

    def _on_algorithm_changed(self, *_):
        """Muestra/oculta Semilla 2 y Constante (a) según el algoritmo elegido."""
        alg_name = self.combo_alg.get()
        gen_cls = Registry.generators.get(alg_name)
        need_two = getattr(gen_cls, "required_seeds", 1) == 2
        need_const = getattr(gen_cls, "requires_constant", False)

        # Posiciones para que todo quepa
        # Semilla 2 en columnas 6-7
        if need_two:
            self.lbl_seed2.grid(row=0, column=6, padx=6, pady=8, sticky="e")
            self.entry_seed2.grid(row=0, column=7, padx=6, pady=8, sticky="w")
        else:
            self.lbl_seed2.grid_forget()
            self.entry_seed2.grid_forget()

        # Constante (a) en columnas 8-9
        if need_const:
            self.lbl_const.grid(row=0, column=8, padx=6, pady=8, sticky="e")
            self.entry_const.grid(row=0, column=9, padx=6, pady=8, sticky="w")
        else:
            self.lbl_const.grid_forget()
            self.entry_const.grid_forget()

    def on_generate(self) -> None:
        try:
            n = int(self.entry_n.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Entrada inválida", "n debe ser un entero positivo.")
            return

        alg_name = self.combo_alg.get()
        if not alg_name:
            messagebox.showerror("Algoritmo", "Selecciona un algoritmo de la lista.")
            return

        gen_cls = Registry.generators.get(alg_name)
        if gen_cls is None:
            messagebox.showerror("Algoritmo", f"Algoritmo '{alg_name}' no encontrado.")
            return

        need_two = getattr(gen_cls, "required_seeds", 1) == 2
        need_const = getattr(gen_cls, "requires_constant", False)

        seed1 = self._parse_int_or_none(self.entry_seed1.get())
        seed2 = self._parse_int_or_none(self.entry_seed2.get()) if need_two else None
        const_a = self._parse_int_or_none(self.entry_const.get()) if need_const else None

        # Validaciones
        if seed1 is None:
            messagebox.showerror("Semilla", "Ingresa una semilla válida (entera).")
            return

        if need_two:
            if seed2 is None:
                messagebox.showerror("Semillas", "Este algoritmo requiere dos semillas (X0 y X1).")
                return
            D1 = len(str(abs(seed1)))
            D2 = len(str(abs(seed2)))
            if D1 != D2 or D1 <= 3:
                messagebox.showerror("Semillas",
                    f"Ambas semillas deben tener el mismo número de dígitos D>3. Recibido D1={D1}, D2={D2}.")
                return

        if need_const:
            if const_a is None:
                messagebox.showerror("Constante (a)", "Debes ingresar la constante 'a' (entera).")
                return
            D = len(str(abs(const_a)))
            if D <= 3:
                messagebox.showerror("Constante (a)", f"'a' debe tener D>3 dígitos. Recibido D={D}.")
                return

        # Generación
        generator = gen_cls()
        kwargs = {}
        if need_two:
            kwargs["seed2"] = seed2
        if need_const:
            kwargs["const_a"] = const_a

        seq = generator.generate(n=n, seed=seed1, **kwargs)

        # Guardar estado + trazas si el generador las provee
        self.state.sequence = seq
        self.state.params["n"] = n
        self.state.params["seed"] = seed1
        if need_two:
            self.state.params["seed2"] = seed2
        if need_const:
            self.state.params["const_a"] = const_a
        self.state.params["trace"] = getattr(generator, "trace", [])

        # Refrescar UI
        self._fill_table(seq)
        self._update_metrics(seq)
        self._draw_histogram(seq)

        Toast(self, text="Secuencia generada ✔")

    def _fill_table(self, seq: np.ndarray) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        max_rows = min(len(seq), 10000)
        trace = self.state.params.get("trace", [])

        if trace:
            for i, line in enumerate(trace[:max_rows]):
                if i % 500 == 0:
                    self.tree.update_idletasks()
                self.tree.insert("", "end", values=(i, line))
        else:
            for i in range(max_rows):
                if i % 500 == 0:
                    self.tree.update_idletasks()
                self.tree.insert("", "end", values=(i, float(seq[i])))

    def _update_metrics(self, seq: np.ndarray) -> None:
        mu = float(np.mean(seq))
        sd = float(np.std(seq, ddof=1)) if len(seq) > 1 else 0.0
        vmin = float(np.min(seq))
        vmax = float(np.max(seq))
        self.lbl_n.config(text=f"n: {len(seq)}")
        self.lbl_mu.config(text=f"μ: {mu:.6f}")
        self.lbl_sd.config(text=f"σ: {sd:.6f}")
        self.lbl_min.config(text=f"min: {vmin:.6f}")
        self.lbl_max.config(text=f"max: {vmax:.6f}")

    def _draw_histogram(self, seq: np.ndarray) -> None:
        bins = int(self.state.params.get("k", 10))
        draw_histogram(self.figure, seq, bins=bins)
        self.canvas.draw_idle()

    def on_export_csv(self) -> None:
        if self.state.sequence is None:
            messagebox.showwarning("Exportar CSV", "No hay datos para exportar. Genera primero.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Guardar números como CSV"
        )
        if not path:
            return
        export_sequence_to_csv(self.state.sequence, path)
        Toast(self, text="CSV guardado 📄")

    def on_save_png(self) -> None:
        if self.state.sequence is None:
            messagebox.showwarning("Guardar PNG", "No hay gráfico para guardar. Genera primero.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")],
            title="Guardar gráfico como PNG"
        )
        if not path:
            return
        self.figure.savefig(path, dpi=150)
        Toast(self, text="PNG guardado 🖼")
