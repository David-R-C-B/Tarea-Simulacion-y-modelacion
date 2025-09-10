"""
Interfaz base para generadores de números pseudoaleatorios.
Cada nuevo algoritmo debe heredar de RandomGenerator y registrarse en Registry.

Se agrega el atributo de clase `required_seeds` (por defecto 1) para que la GUI
sepa si debe pedir una segunda semilla (p.ej., Productos Medios).
"""
from abc import ABC, abstractmethod
from typing import Optional
import numpy as np

class RandomGenerator(ABC):
    # Cantidad de semillas requeridas por el algoritmo (1 o 2)
    required_seeds: int = 1

    @abstractmethod
    def generate(self, n: int, seed: Optional[int], **kwargs) -> np.ndarray:
        """Genera una secuencia de longitud n. Retorna np.ndarray de floats o ints."""
        raise NotImplementedError
