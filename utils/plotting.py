"""
Histograma con esquema oscuro sobrio (no neón).
"""
from typing import Optional
import numpy as np
from matplotlib.figure import Figure
from gui.theme import PALETTE

def draw_histogram(fig: Figure, data: np.ndarray, bins: int = 10) -> None:
    fig.clear()
    fig.set_facecolor(PALETTE["elev"])
    ax = fig.add_subplot(111)
    ax.set_facecolor(PALETTE["surface"])
    # barras con borde sutil
    ax.hist(data, bins=bins, edgecolor="#2B3547")
    ax.set_title("Histograma", color=PALETTE["text"])
    ax.set_xlabel("Valor", color=PALETTE["subtle"])
    ax.set_ylabel("Frecuencia", color=PALETTE["subtle"])
    ax.tick_params(colors=PALETTE["subtle"])
    for spine in ax.spines.values():
        spine.set_color("#2B3547")
    fig.tight_layout()
