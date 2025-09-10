"""
Widgets custom: barra animada, botones con hover y pequeños toasts.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple
from .theme import PALETTE

class HoverAccentButton(ttk.Button):
    """
    Botón acento con hover suave (sin neón).
    Cambia a 'AccentHover.TButton' al entrar el puntero.
    """
    def __init__(self, master=None, **kwargs):
        super().__init__(master, style="Accent.TButton", **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _):
        self.configure(style="AccentHover.TButton")

    def _on_leave(self, _):
        self.configure(style="Accent.TButton")


class ScanBar(ttk.Frame):
    """
    Barra sutil en la parte superior que anima un 'escaneo' lateral continuo.
    Minimal y sobrio; aporta dinamismo sin distraer.
    """
    def __init__(self, master=None, height: int = 3, speed: int = 6, **kwargs):
        super().__init__(master, style="Header.TFrame", **kwargs)
        self.canvas = tk.Canvas(self, height=height, highlightthickness=0, bd=0,
                                bg=PALETTE["header"])
        self.canvas.pack(fill="x", expand=True)
        self._x = 0
        self._speed = speed
        self._bar = None
        self.bind("<Configure>", self._on_resize)
        self.after(300, self._tick)

    def _on_resize(self, _):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        # barra de 22% del ancho
        bw = max(60, int(w * 0.22))
        self._bar = self.canvas.create_rectangle(-bw, 0, 0, h, fill=PALETTE["accent"], width=0)

    def _tick(self):
        if self._bar is None:
            self.after(120, self._tick)
            return
        w = self.canvas.winfo_width()
        bw = int(w * 0.22)
        self._x = (self._x + self._speed) % (w + bw)
        self.canvas.coords(self._bar, self._x - bw, 0, self._x, self.canvas.winfo_height())
        self.after(24, self._tick)  # ~40fps suave


class Toast(ttk.Frame):
    """
    Mensaje flotante que aparece y se desvanece (para confirmaciones).
    """
    def __init__(self, master, text: str, duration_ms: int = 1600):
        super().__init__(master, style="TLabelframe")
        self.label = ttk.Label(self, text=text, style="TLabel")
        self.label.pack(padx=12, pady=8)
        self.duration = duration_ms
        self.after(10, self._place_and_fade_in)

    def _place_and_fade_in(self):
        parent = self.master
        w = parent.winfo_width()
        h = parent.winfo_height()
        self.place(x=w-320, y=h-100)  # esquina inferior derecha
        # Fade-in simulando pasos de opacidad via colores (limitación de tkinter por-widget)
        steps = 6
        for i in range(steps):
            self.after(i*22, lambda ii=i: self.label.configure(foreground=self._mix(ii/steps)))

        self.after(self.duration, self._fade_out)

    def _mix(self, t: float) -> str:
        # interpola color entre 'subtle' y 'text' para simular entrada
        import colorsys
        def hex_to_rgb(h): return tuple(int(h[i:i+2], 16) for i in (1,3,5))
        def rgb_to_hex(r,g,b): return f"#{r:02X}{g:02X}{b:02X}"
        a = hex_to_rgb(PALETTE["subtle"])
        b = hex_to_rgb(PALETTE["text"])
        c = tuple(int(a[i]*(1-t) + b[i]*t) for i in range(3))
        return rgb_to_hex(*c)

    def _fade_out(self):
        steps = 6
        for i in range(steps):
            self.after(i*22, lambda ii=i: self.label.configure(foreground=self._mix(1 - ii/steps)))
        self.after(steps*22 + 40, self.destroy)
