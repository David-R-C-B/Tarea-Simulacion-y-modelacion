"""
Estado global de la aplicación: secuencia actual, parámetros y resultados.
Se centraliza aquí para que las pestañas compartan datos sin acoplarse fuerte.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import numpy as np

@dataclass
class AppState:
    sequence: Optional[np.ndarray] = None

    params: Dict[str, Any] = field(default_factory=lambda: {
        "n": 1000,
        "seed": None,
        "k": 10,
        "alpha": 0.05,
    })

    # Cada item puede incluir: i, x_prev, y, x_next, r, display
    generation_trace: List[Dict[str, Any]] = field(default_factory=list)

    # Resultados de pruebas
    test_results: List[Dict[str, Any]] = field(default_factory=list)

