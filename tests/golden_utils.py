"""Utilidades para golden tests (approval testing) y equivalencia de SQL."""

import difflib
import os
import re
from pathlib import Path

import pytest

ACTUALIZAR = os.environ.get("ACTUALIZAR_GOLDEN") == "1"
_IGNORAR_EN_DATOS = re.compile(r"^(SET |SELECT TO_CHAR\(SYSDATE|/$|COMMIT;$)")


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


def sentencias(sql: str, *, solo_logica: bool = False) -> list[str]:
    """Líneas normalizadas: sin comentarios ni diferencias de espacios o mayúsculas.

    Con solo_logica se omiten las líneas de control de SQL*Plus (SET, hora, '/', COMMIT),
    cuyo formato cambió a propósito con el estándar.
    """
    resultado = []
    for linea in sql.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("--"):
            continue
        linea = re.sub(r"\s+", " ", linea).upper()
        linea = re.sub(r"\s*([(),=])\s*", r"\1", linea)
        if solo_logica and _IGNORAR_EN_DATOS.match(linea):
            continue
        resultado.append(linea)
    return resultado


def corregir(lineas: list[str], correcciones: list[tuple[str, str]]) -> list[str]:
    """Aplica al original las correcciones intencionales del estándar."""
    for antes, despues in correcciones:
        lineas = [linea.replace(antes, despues) for linea in lineas]
    return lineas


def verificar_equivalencia(generado: list[str], original: list[str]) -> None:
    if generado != original:
        diferencias = difflib.unified_diff(original, generado, "original", "generado", lineterm="")
        pytest.fail("Las sentencias difieren del original:\n" + "\n".join(diferencias))
