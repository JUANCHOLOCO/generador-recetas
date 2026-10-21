"""Utilidades para golden tests (approval testing) y equivalencia de SQL."""

import difflib
import os
import re
from pathlib import Path

import pytest

ACTUALIZAR = os.environ.get("ACTUALIZAR_GOLDEN") == "1"


def verificar_golden(esperado: Path, obtenido: bytes) -> None:
    """Compara byte a byte con el archivo aprobado. Con ACTUALIZAR_GOLDEN=1 lo (re)escribe."""
    if ACTUALIZAR:
        esperado.parent.mkdir(parents=True, exist_ok=True)
        esperado.write_bytes(obtenido)
        return
    if not esperado.exists():
        pytest.fail(f"No existe {esperado}. Genérelo con ACTUALIZAR_GOLDEN=1 y revíselo.")
    if esperado.read_bytes() != obtenido:
        diferencias = difflib.unified_diff(
            esperado.read_bytes().decode("cp1252").splitlines(),
            obtenido.decode("cp1252").splitlines(),
            "esperado",
            "obtenido",
            lineterm="",
        )
        pytest.fail("\n".join(diferencias))


def leer_original(ruta: Path) -> str:
    """Los originales mezclan UTF-8 y cp1252: se intenta UTF-8 primero."""
    datos = ruta.read_bytes()
    try:
        return datos.decode("utf-8")
    except UnicodeDecodeError:
        return datos.decode("cp1252")


def sentencias(sql: str) -> list[str]:
    """Sentencias normalizadas: sin comentarios, líneas vacías ni diferencias de espaciado."""
    resultado = []
    for linea in sql.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("--"):
            continue
        resultado.append(re.sub(r"\s+", " ", linea).upper())
    return resultado