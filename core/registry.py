"""
Registro global de plugins (generadores y pruebas) sin dependencias
de runtime hacia 'tests.*' ni 'generators.*' para evitar imports circulares.
"""

from typing import Dict, Any, Callable

class Registry:
    # Guardamos callables (clases o fábricas). No tipamos con clases concretas
    # para no forzar imports en tiempo de carga.
    generators: Dict[str, Callable[..., Any]] = {}
    tests: Dict[str, Callable[[], Any]] = {}

    @classmethod
    def register_generator(cls, name: str, gen_callable: Callable[..., Any]) -> None:
        """
        Registra un generador. Normalmente se pasa la clase del generador.
        Ej.: Registry.register_generator("Cuadrados Medios", MidSquare)
        """
        cls.generators[name] = gen_callable

    @classmethod
    def register_test(cls, name: str, test_factory: Callable[[], Any]) -> None:
        """
        Registra una prueba. Puede ser la clase (callable) o una lambda fábrica.
        Ej.: Registry.register_test("Varianza χ²", lambda: VarianceChiSquare())
        """
        cls.tests[name] = test_factory
