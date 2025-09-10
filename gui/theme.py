"""
Tema oscuro minimalista estilo 'cyberpunk serio' (sin neón).
Aplica colores sobrios, tipografía moderna y estilos ttk coherentes.
"""
import tkinter as tk
from tkinter import ttk

PALETTE = {
    "bg":        "#0E1014",  # fondo ventana
    "surface":   "#151923",  # paneles
    "elev":      "#1B2230",  # elevación ligera
    "muted":     "#242D3B",  # bordes/contornos
    "text":      "#E6EAF2",  # texto principal
    "subtle":    "#9AA9BF",  # texto secundario
    "accent":    "#52C9BB",  # acento turquesa tenue
    "accent2":   "#A678B4",  # acento morado tenue
    "warn":      "#E3C26D",
    "error":     "#E26D6D",
    "header":    "#0B0D11",
    "focus":     "#5FD3C6",
}

FONTS = {
    "base": ("Segoe UI", 10),
    "mono": ("Consolas", 10),
    "title": ("Segoe UI Semibold", 12),
    "big": ("Segoe UI Semibold", 14),
}

def _style_button(style: ttk.Style):
    # Botón base
    style.configure(
        "TButton",
        font=FONTS["base"],
        padding=(12, 8),
        background=PALETTE["muted"],
        foreground=PALETTE["text"],
        borderwidth=0,
        focusthickness=3,
        focuscolor=PALETTE["focus"]
    )
    style.map(
        "TButton",
        background=[("active", "#2B3547")],
        relief=[("pressed", "sunken")]
    )

    # Botón acento
    style.configure(
        "Accent.TButton",
        background=PALETTE["accent"],
        foreground="#0B0D11"
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#6ED9CE")]
    )

    # Hover alterno para Accent
    style.configure(
        "AccentHover.TButton",
        background="#6ED9CE",
        foreground="#0B0D11"
    )

def _style_frames(style: ttk.Style):
    for s in ("TFrame", "TLabelframe", "TLabelframe.Label"):
        style.configure(s, background=PALETTE["surface"], foreground=PALETTE["text"])
    style.configure("Root.TFrame", background=PALETTE["bg"])
    style.configure("Header.TFrame", background=PALETTE["header"])

def _style_labels(style: ttk.Style):
    style.configure("TLabel", background=PALETTE["surface"], foreground=PALETTE["text"], font=FONTS["base"])
    style.configure("Subtle.TLabel", foreground=PALETTE["subtle"])
    style.configure("Title.TLabel", font=FONTS["big"])
    style.configure("Metric.TLabel", background=PALETTE["elev"], padding=(10, 6), font=FONTS["base"])

def _style_entries(style: ttk.Style):
    style.configure(
        "TEntry",
        fieldbackground="#0F141E",
        foreground=PALETTE["text"],
        bordercolor=PALETTE["muted"],
        lightcolor=PALETTE["focus"],
        darkcolor=PALETTE["muted"],
        padding=8
    )

def _style_notebook(style: ttk.Style):
    style.configure("TNotebook", background=PALETTE["bg"], borderwidth=0)
    style.configure("TNotebook.Tab", padding=(16, 8), background=PALETTE["surface"], foreground=PALETTE["subtle"])
    style.map(
        "TNotebook.Tab",
        foreground=[("selected", PALETTE["text"])],
        background=[("selected", PALETTE["elev"])]
    )

def _style_tree(style: ttk.Style):
    style.configure(
        "Treeview",
        background=PALETTE["elev"],
        fieldbackground=PALETTE["elev"],
        foreground=PALETTE["text"],
        bordercolor=PALETTE["muted"],
        rowheight=24,
        font=FONTS["mono"]
    )
    style.configure(
        "Treeview.Heading",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=("Segoe UI Semibold", 10)
    )

def _style_progress(style: ttk.Style):
    style.configure(
        "Horizontal.TProgressbar",
        troughcolor=PALETTE["muted"],
        background=PALETTE["accent"]
    )

def apply_theme(root: tk.Tk) -> None:
    root.configure(bg=PALETTE["bg"])
    style = ttk.Style(root)
    # 'clam' es más consistente para personalizaciones
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    _style_frames(style)
    _style_labels(style)
    _style_button(style)
    _style_entries(style)
    _style_notebook(style)
    _style_tree(style)
    _style_progress(style)
