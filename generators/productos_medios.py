"""
Generador – Productos Medios (Middle Product) con trazado de pasos.

Reglas:
1) Ingresar X0 con D dígitos (D>3)
2) Ingresar X1 con D dígitos (D>3)
3) Y0 = X0 * X1 ; X2 = D dígitos del centro de Y0 ; r2 = 0.(D-dígitos)
4) Y1 = X1 * X2 ; X3 = D dígitos del centro de Y1 ; r3 = 0.(D-dígitos)
5) Repetir ...

Notas:
- Ambas semillas deben tener el MISMO D (>3).
- Al formar Y no se rellena a 2D. Solo si len(str(Y)) es impar, se antepone '0'.
- Se toman siempre los D dígitos centrales para el siguiente X.
"""
from typing import Optional
import numpy as np
from generators.base import RandomGenerator
from core.registry import Registry

class MiddleProduct(RandomGenerator):
    required_seeds = 2  # requiere dos semillas

    def __init__(self):
        # Ejemplo de línea:
        # Y0=(5735)*(1017)=583...   X2=abcd   r2=0.abcd
        self.trace = []

    def generate(self, n: int, seed: Optional[int], **kwargs) -> np.ndarray:
        seed2 = kwargs.get("seed2", None)
        if seed is None or seed2 is None:
            raise ValueError("Productos Medios requiere dos semillas enteras (X0 y X1) con D>3 dígitos.")

        s1 = str(abs(int(seed)))
        s2 = str(abs(int(seed2)))
        D1, D2 = len(s1), len(s2)
        if D1 != D2 or D1 <= 3:
            raise ValueError(f"Ambas semillas deben tener el mismo número de dígitos D>3. "
                             f"Recibido D1={D1}, D2={D2}.")

        D = D1
        base = 10 ** D
        out = np.empty(n, dtype=float)
        self.trace.clear()

        x_prev = int(seed)   # X0
        x_curr = int(seed2)  # X1

        for j in range(n):
            x_prev_str = str(x_prev).zfill(D)
            x_curr_str = str(x_curr).zfill(D)

            y = x_prev * x_curr
            y_str = str(y)
            if len(y_str) % 2 == 1:  # solo si impar, anteponer '0'
                y_str = "0" + y_str

            L = len(y_str)
            start = (L - D) // 2
            mid = y_str[start:start + D]  # X_{j+2}
            x_next = int(mid)
            r = x_next / base
            out[j] = r

            # Guardar paso: Yj=(Xj)*(Xj+1)=...   X{j+2}=mid   r{j+2}=0.mid
            self.trace.append(
                f"Y{j}=({x_prev_str})*({x_curr_str})={y_str}   X{j+2}={mid}   r{j+2}=0.{mid}"
            )

            # desplazar
            x_prev, x_curr = x_curr, x_next

        return out

# Registrar en el catálogo
Registry.register_generator("Productos Medios (Middle Product)", MiddleProduct)
