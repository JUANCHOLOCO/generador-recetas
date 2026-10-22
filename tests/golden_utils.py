"""Utilidades para golden tests (approval testing) y equivalencia de SQL."""

import difflib
import os
import re
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

ACTUALIZAR = os.environ.get("ACTUALIZAR_GOLDEN") == "1"
_CONTROL_SQLPLUS = re.compile(r"^(SET |SELECT TO_CHAR\(SYSDATE|/$|COMMIT;?$)")

Correccion = Callable[[list[str]], list[str]]


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


def _normalizar(texto: str) -> str:
    texto = re.sub(r"\s+", " ", texto.strip()).upper()
    return re.sub(r"\s*([(),=])\s*", r"\1", texto)


def _lineas_utiles(sql: str) -> list[str]:
    return [
        _normalizar(linea)
        for linea in sql.splitlines()
        if linea.strip() and not linea.strip().startswith("--")
    ]


def sentencias(sql: str) -> list[str]:
    """Líneas normalizadas. Para los wrappers, donde se comparan todas las líneas."""
    return _lineas_utiles(sql)


def sentencias_sql(sql: str) -> list[str]:
    """Sentencias de un script de datos, sin el control de SQL*Plus (SET, hora, '/', COMMIT).

    Une las líneas y corta por ';', así una sentencia escrita en 1 o en 19 líneas
    se compara igual.
    """
    lineas = [linea for linea in _lineas_utiles(sql) if not _CONTROL_SQLPLUS.match(linea)]
    partes = (_normalizar(parte) for parte in " ".join(lineas).split(";"))
    return [parte for parte in partes if parte]


def reemplazar(antes: str, despues: str) -> Correccion:
    """Corrección simple: reemplaza un texto en todas las sentencias."""

    def aplicar(lista: list[str]) -> list[str]:
        return [s.replace(antes, despues) for s in lista]

    return aplicar


def corregir(lista: list[str], correcciones: Sequence[Correccion]) -> list[str]:
    """Aplica al original, en orden, las correcciones intencionales del estándar."""
    for correccion in correcciones:
        lista = correccion(lista)
    return lista


def verificar_equivalencia(generado: list[str], original: list[str]) -> None:
    if generado != original:
        diferencias = difflib.unified_diff(original, generado, "original", "generado", lineterm="")
        pytest.fail("Las sentencias difieren del original:\n" + "\n".join(diferencias))
