"""
Prueba de medias (Z) para uniformidad en [0,1].

Estadístico:
  Z = sqrt(12 n) * ( ū - 0.5 )
Decisión (bilateral, nivel α):
  Aceptar H0 si |Z| ≤ z_{1-α/2}

También se reporta p-value bilateral:
  p = 2 * (1 - Φ(|Z|))

Validaciones:
- Advertencia si n<10.
- Advertencia si hay valores fuera de (0,1).
"""
from typing import Dict, Any, List
import numpy as np
from scipy.stats import norm

from tests.base import RandomnessTest
from core.registry import Registry

class MeanZTest(RandomnessTest):
    def run(self, sequence: np.ndarray, **kwargs) -> Dict[str, Any]:
        alpha: float = float(kwargs.get("alpha", 0.05))
        u = np.asarray(sequence, dtype=float)

        n = u.size
        warnings: List[str] = []
        if n < 10:
            warnings.append("n<10: la prueba de medias puede no ser fiable (muestra pequeña).")

        if not np.all((u > 0.0) & (u < 1.0)):
            warnings.append("Se detectaron valores fuera de (0,1); la hipótesis Uniforme[0,1] queda comprometida.")

        ubar = float(np.mean(u)) if n > 0 else float("nan")
        # Z = sqrt(12 n) * ( ū - 0.5 )
        Z = float(np.sqrt(12.0 * n) * (ubar - 0.5)) if n > 0 else float("nan")

        # Crítico bilateral
        zcrit = float(norm.ppf(1.0 - alpha / 2.0))
        # p-value bilateral
        pval = float(2.0 * (1.0 - norm.cdf(abs(Z)))) if np.isfinite(Z) else float("nan")
        accept = abs(Z) <= zcrit if np.isfinite(Z) else False

        result: Dict[str, Any] = {
            "test": "Medias Z (Uniforme[0,1])",
            "alpha": alpha,
            "n": n,
            "mean": ubar,
            "Z": Z,
            "z_crit_(1-alpha/2)": zcrit,
            "p_value": pval,
            "conclusion": ("Pasa la prueba de medias a nivel α" if accept else "No pasa la prueba de medias a nivel α"),
            "status": "ok",
        }
        if warnings:
            result["warnings"] = warnings
            result["status"] = "warning"
        return result

# Registrar en el catálogo de pruebas (nombre correcto: Prueba de medias)
Registry.register_test("Medias Z (Uniforme[0,1])", lambda: MeanZTest())
