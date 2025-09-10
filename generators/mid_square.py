"""
Generador – Cuadrados Medios (Mid-Square) con trazado de pasos.

Regla:
- Al formar Y = X^2 NO se rellena a 2D. Solo si len(str(Y)) es impar,
  se antepone un '0' para tener longitud par. Luego se toman los D
  dígitos centrales. Si len(Y) es 6 y D=4, se toman directamente esos 4
  del medio (sin añadir '00').

Además expone self.trace con líneas tipo:
  Y0=(X0)^2=resultado   X1=dddd   r1=0.dddd
para que la GUI pueda mostrar los pasos en la tabla.
"""
from typing import Optional
import numpy as np
from generators.base import RandomGenerator
from core.registry import Registry

class MidSquare(RandomGenerator):
    required_seeds = 1  # <- una sola semilla

    def __init__(self):
        self.trace = []  # lista de strings, una por fila/iteración

    def generate(self, n: int, seed: Optional[int], **kwargs) -> np.ndarray:
        if seed is None:
            raise ValueError("Cuadrados Medios requiere semilla entera (X0) con D>3 dígitos.")

        # D = cantidad de dígitos de la semilla (base 10)
        s = str(abs(int(seed)))
        D = len(s)
        if D <= 3:
            raise ValueError(f"La semilla debe tener D>3 dígitos. Semilla '{seed}' tiene D={D}.")

        x = int(seed)
        out = np.empty(n, dtype=float)
        base = 10 ** D
        self.trace.clear()

        for j in range(n):
            x_str_D = str(x).zfill(D)  # solo para mostrar Xj con D dígitos
            y = x * x
            y_str = str(y)             # NO rellenar a 2D
            if len(y_str) % 2 == 1:    # solo si impar, anteponer un '0'
                y_str = "0" + y_str

            L = len(y_str)
            start = (L - D) // 2       # índice inicial del bloque central de tamaño D
            mid = y_str[start:start + D]  # Xi+1 (D dígitos)
            x = int(mid)
            r = x / base
            out[j] = r

            # Guardar paso legible
            self.trace.append(
                f"Y{j}=({x_str_D})^2={y_str}   X{j+1}={mid}   r{j+1}=0.{mid}"
            )

        return out

# Registrar en el catálogo
Registry.register_generator("Cuadrados Medios (Mid-Square)", MidSquare)
