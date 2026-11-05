import sqlite3
from datetime import datetime
from pathlib import Path

import pytest

from recetas.core.infrastructure.db.respaldo import respaldar

pytestmark = pytest.mark.integration

AHORA = datetime(2026, 11, 4, 21, 30, 5)


def _base_con_un_canal(ruta: Path) -> Path:
    conexion = sqlite3.connect(ruta)
    try:
        conexion.execute("CREATE TABLE canal (nombre TEXT)")
        conexion.execute("INSERT INTO canal VALUES ('Retail')")
        conexion.commit()
    finally:
        conexion.close()
    return ruta


def test_sin_base_no_hay_respaldo(tmp_path: Path) -> None:
    assert respaldar(tmp_path / "recetas.db", tmp_path / "backups", AHORA) is None
    assert not (tmp_path / "backups").exists()


def test_respalda_con_fecha_y_hora_y_el_mismo_contenido(tmp_path: Path) -> None:
    base = _base_con_un_canal(tmp_path / "recetas.db")

    destino = respaldar(base, tmp_path / "backups", AHORA)

    assert destino == tmp_path / "backups" / "recetas_20261104_213005.db"
    conexion = sqlite3.connect(destino)
    try:
        assert conexion.execute("SELECT nombre FROM canal").fetchall() == [("Retail",)]
    finally:
        conexion.close()


def test_conserva_solo_los_mas_recientes(tmp_path: Path) -> None:
    base = _base_con_un_canal(tmp_path / "recetas.db")
    carpeta = tmp_path / "backups"
    carpeta.mkdir()
    for viejo in ["recetas_20260101_000000.db", "recetas_20260201_000000.db"]:
        (carpeta / viejo).write_bytes(b"")

    respaldar(base, carpeta, AHORA, conservar=2)

    assert sorted(p.name for p in carpeta.iterdir()) == [
        "recetas_20260201_000000.db",
        "recetas_20261104_213005.db",
    ]
