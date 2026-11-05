"""Copia de seguridad de la base SQLite antes de migrarla."""

import sqlite3
from datetime import datetime
from pathlib import Path

CONSERVAR = 10


def respaldar(
    base: Path, carpeta: Path, ahora: datetime, conservar: int = CONSERVAR
) -> Path | None:
    """Copia la base a <carpeta>/recetas_AAAAMMDD_HHMMSS.db y borra los respaldos más viejos.

    No hace nada si la base todavía no existe (primer arranque).
    """
    if not base.exists():
        return None
    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / f"{base.stem}_{ahora:%Y%m%d_%H%M%S}.db"
    origen = sqlite3.connect(base)
    copia = sqlite3.connect(destino)
    try:
        origen.backup(copia)
    finally:
        copia.close()
        origen.close()
    for viejo in sorted(carpeta.glob(f"{base.stem}_*.db"))[:-conservar]:
        viejo.unlink()
    return destino
