"""
Interfaz base para pruebas estadísticas.
Cada prueba debe heredar y exponer `run(sequence, **kwargs) -> dict`.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import numpy as np

class RandomnessTest(ABC):
    @abstractmethod
    def run(self, sequence: np.ndarray, **kwargs) -> Dict[str, Any]:
        """Ejecuta la prueba y retorna un dict con resultados y conclusiones."""
        raise NotImplementedError
