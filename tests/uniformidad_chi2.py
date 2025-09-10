"""
Prueba de uniformidad (chi-cuadrado) para U(0,1).

Entrada:
- sequence: np.ndarray de números en [0,1] (idealmente).
- alpha: nivel de significancia (default 0.05).
- m: número de clases/intervalos (opcional).
      Si no se indica, m = floor(sqrt(n)).
      Se intenta asegurar E_i = n/m >= 5 ajustando m hacia abajo.
      Si el usuario fija m y n/m<5, se reduce m y se advierte.

Pasos:
1) Validar rango [0,1] (advertencia si hay valores fuera).
2) Construir m intervalos equiprobables: [0,1/m), [1/m,2/m), ..., [(m-1)/m,1]
3) Calcular O_i (frecuencias observadas) y E_i = n/m.
4) Estadístico: chi2_stat = sum (O_i - E_i)^2 / E_i
5) df = m - 1  (no se estiman parámetros).
6) Crítico: chi2_crit = chi2.ppf(1 - alpha, df)  (cuantil derecho).
7) p-value: p = 1 - F_{chi2,df}(chi2_stat)
8) Decisión: no rechazar H0 si chi2_stat <= chi2_crit.

Devuelve:
- Tabla por intervalo con: [a_i,b_i], O_i, E_i, contribución.
- n, m, df, alpha, chi2_stat, chi2_crit, p_value y conclusión.
"""
from typing import Dict, Any, List, Optional
import numpy as np
from scipy.stats import chi2

from tests.base import RandomnessTest
from core.registry import Registry

class UniformityChiSquare(RandomnessTest):
    def run(self, sequence: np.ndarray, **kwargs) -> Dict[str, Any]:
        alpha: float = float(kwargs.get("alpha", 0.05))
        m_user: Optional[int] = kwargs.get("m", None)

        u = np.asarray(sequence, dtype=float)
        n = int(u.size)
        warnings: List[str] = []

        if n < 10:
            warnings.append("n<10: la prueba chi² puede no ser fiable (muestra pequeña).")

        # Rango
        if not np.all((u >= 0.0) & (u <= 1.0)):
            warnings.append("Se detectaron valores fuera de [0,1]; la prueba se aplica sobre [0,1].")

        # Elegir m
        if m_user is None:
            m = int(np.floor(np.sqrt(n))) if n > 0 else 1
            m = max(2, m)
            # asegurar E_i >= 5 si es posible: m <= n/5
            if n >= 10:
                m = min(m, max(2, n // 5))
        else:
            m = int(m_user)
            if m < 2:
                warnings.append("m<2 no es válido; se ajusta a m=2.")
                m = 2
            if n >= 10 and n / m < 5:
                m_new = max(2, n // 5)
                if m_new < m:
                    warnings.append(f"m={m_user} produce E_i=n/m<5; se ajusta a m={m_new}.")
                    m = m_new

        # Bordes de los intervalos (último cerrado en 1)
        edges = np.linspace(0.0, 1.0, m + 1)
        # Histograma: numpy deja el último intervalo cerrado en el borde derecho
        O, _ = np.histogram(u, bins=edges)
        O = O.astype(int)
        E = n / m if m > 0 else np.nan

        # Contribuciones y estadístico
        with np.errstate(divide="ignore", invalid="ignore"):
            contrib = ((O - E) ** 2) / E if E > 0 else np.full_like(O, np.nan, dtype=float)
        chi2_stat = float(np.nansum(contrib))

        df = max(m - 1, 1)
        chi2_crit = float(chi2.ppf(1.0 - alpha, df))
        p_value = float(1.0 - chi2.cdf(chi2_stat, df))

        accept = chi2_stat <= chi2_crit

        # Tabla por intervalo
        table: List[Dict[str, Any]] = []
        for i in range(m):
            a_i = float(edges[i])
            b_i = float(edges[i + 1])
            # formato de intervalo: [a,b) excepto el último [a,b]
            interval = f"[{a_i:.4f}, {b_i:.4f}{')' if i < m-1 else ']'}"
            table.append({
                "interval": interval,
                "O_i": int(O[i]),
                "E_i": float(E),
                "term": float(contrib[i]),
            })

        result: Dict[str, Any] = {
            "test": "Uniformidad χ² (Uniforme[0,1])",
            "alpha": alpha,
            "n": n,
            "m": m,
            "df": df,
            "chi2_stat": chi2_stat,
            "chi2_crit_(1-alpha,df)": chi2_crit,
            "p_value": p_value,
            "decision": ("No se rechaza H0 (pasa uniformidad)" if accept else "Se rechaza H0 (no pasa uniformidad)"),
            "table": table,
            "status": "ok",
        }
        if n / m < 5:
            warnings.append(f"E_i = n/m = {n/m:.2f} < 5; los resultados pueden ser inexactos.")
        if warnings:
            result["warnings"] = warnings
            result["status"] = "warning"
        return result

# Registro en catálogo
Registry.register_test("Uniformidad χ² (Uniforme[0,1])", lambda: UniformityChiSquare())
