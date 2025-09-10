"""
Prueba de varianza (chi-cuadrado) para uniformidad en [0,1].

Pasos:
1) n, media ū y varianza muestral insesgada S^2.
2) σ0^2 = 1/12 ; Q = (n-1) S^2 / σ0^2.
3) df = n-1 ; cuantiles χ^2_{α/2,df} y χ^2_{1-α/2,df}.
4) Acepta H0 si χ^2_{α/2,df} ≤ Q ≤ χ^2_{1-α/2,df}.
5) Intervalo de aceptación para S^2.
6) p-value bilateral.

Validaciones:
- Advertencia si n<10.
- Advertencia si hay valores fuera de (0,1).
"""
from typing import Dict, Any, List
import numpy as np
from scipy.stats import chi2

from tests.base import RandomnessTest
from core.registry import Registry

class VarianceChiSquare(RandomnessTest):
    def run(self, sequence: np.ndarray, **kwargs) -> Dict[str, Any]:
        alpha: float = float(kwargs.get("alpha", 0.05))
        u = np.asarray(sequence, dtype=float)

        n = u.size
        warnings: List[str] = []
        if n < 10:
            warnings.append("n<10: la prueba puede no ser fiable (muestra pequeña).")

        if not np.all((u > 0.0) & (u < 1.0)):
            warnings.append("Se detectaron valores fuera de (0,1); la hipótesis Uniforme[0,1] queda comprometida.")

        ubar = float(np.mean(u)) if n > 0 else float("nan")
        S2 = float(np.var(u, ddof=1)) if n > 1 else float("nan")

        sigma0_sq = 1.0 / 12.0
        df = max(n - 1, 1)
        Q = float(((n - 1) * S2) / sigma0_sq) if n > 1 else float("nan")

        chi2_lower = float(chi2.ppf(alpha / 2.0, df))
        chi2_upper = float(chi2.ppf(1.0 - alpha / 2.0, df))

        S2_low = sigma0_sq * chi2_lower / (n - 1) if n > 1 else float("nan")
        S2_high = sigma0_sq * chi2_upper / (n - 1) if n > 1 else float("nan")

        FQ = float(chi2.cdf(Q, df)) if np.isfinite(Q) else float("nan")
        pval = float(2.0 * min(FQ, 1.0 - FQ)) if np.isfinite(FQ) else float("nan")
        pval = max(min(pval, 1.0), 0.0) if np.isfinite(pval) else pval

        accept = (chi2_lower <= Q <= chi2_upper) if np.isfinite(Q) else False

        result: Dict[str, Any] = {
            "test": "Varianza χ² (Uniforme[0,1])",
            "alpha": alpha,
            "n": n,
            "mean": ubar,
            "S2": S2,
            "sigma0_sq": sigma0_sq,
            "Q": Q,
            "df": df,
            "chi2_lower": chi2_lower,
            "chi2_upper": chi2_upper,
            "accept_interval_S2": [S2_low, S2_high],
            "p_value": pval,
            "conclusion": ("Pasa la prueba de varianza a nivel α" if accept else "No pasa la prueba de varianza a nivel α"),
            "status": "ok",
        }
        if warnings:
            result["warnings"] = warnings
            result["status"] = "warning"
        return result

# Registrar en el catálogo
Registry.register_test("Varianza χ² (Uniforme[0,1])", lambda: VarianceChiSquare())
