"""
Generador – Multiplicador Constante (Constant Multiplier) con trazado de pasos.

Reglas:
1) Ingresar una semilla X0 (entera).
2) Elegir una constante 'a' con D dígitos (D > 3).
3) Y0 = a * X0 ; X1 = D dígitos del centro de Y0 ; r1 = 0.(D dígitos)
4) Y1 = a * X1 ; X2 = D dígitos del centro de Y1 ; r2 = 0.(D dígitos)
5) Repetir...

Detalles:
- D se define por la cantidad de dígitos de 'a'. Debe ser D>3.
- Al formar Y = a * X, NO se rellena a 2D. Solo si len(Y) es impar,
  se antepone '0' para tener longitud par. Luego se toman los D dígitos
  centrales.
- La semilla puede tener cualquier número de dígitos; para la trazabilidad
  se muestra con padding a D (zfill(D)).
"""
from typing import Optional
import numpy as np
from generators.base import RandomGenerator
from core.registry import Registry

class ConstantMultiplier(RandomGenerator):
    required_seeds = 1
    requires_constant = True

    def __init__(self):
        # Ej.: "Y0=(a)*(X0)=resultado   X1=dddd   r1=0.dddd"
        self.trace = []

    def generate(self, n: int, seed: Optional[int], **kwargs) -> np.ndarray:
        if seed is None:
            raise ValueError("Multiplicador Constante requiere una semilla entera X0.")
        const_a = kwargs.get("const_a", None)
        if const_a is None:
            raise ValueError("Debes proporcionar la constante 'a' con D>3 dígitos.")

        a = int(const_a)
        a_str = str(abs(a))
        D = len(a_str)
        if D <= 3:
            raise ValueError(f"La constante 'a' debe tener D>3 dígitos. Recibido D={D}.")

        base = 10 ** D
        out = np.empty(n, dtype=float)
        self.trace.clear()

        x = int(seed)
        for j in range(n):
            x_str = str(x).zfill(D)
            a_str_pad = a_str.zfill(D)

            y = a * x
            y_str = str(y)
            if len(y_str) % 2 == 1:        # solo si impar, anteponer '0'
                y_str = "0" + y_str

            L = len(y_str)
            start = (L - D) // 2
            mid = y_str[start:start + D]   # X_{j+1}
            x = int(mid)
            r = x / base
            out[j] = r

            self.trace.append(
                f"Y{j}=({a_str_pad})*({x_str})={y_str}   X{j+1}={mid}   r{j+1}=0.{mid}"
            )

        return out

# Registrar en el catálogo
Registry.register_generator("Multiplicador Constante", ConstantMultiplier)
