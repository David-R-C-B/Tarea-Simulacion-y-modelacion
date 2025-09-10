"""
Exportación de resultados a CSV y guardado de gráficos a PNG.
"""
from typing import Sequence
import csv
import pathlib

def export_sequence_to_csv(numbers: Sequence[float], path: str) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "value"])
        for i, x in enumerate(numbers):
            writer.writerow([i, x])

# La exportación de gráficos se hace desde utils.plotting (ver abajo)
