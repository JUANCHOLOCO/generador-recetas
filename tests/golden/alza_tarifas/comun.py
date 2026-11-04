"""Utilidades de los golden del alza TPFB-1726."""

import re
from decimal import Decimal
from pathlib import Path

from recetas.core.infrastructure.templating.jinja import JinjaRenderer

CASO = Path(__file__).parent / "TPFB-1726"
RENDERER = JinjaRenderer("recetas.modules.alza_tarifas", "recetas.core")
_NUMERO_ENTRE_COMILLAS = re.compile(r"'(\d+(?:,\d+)?)'")


def sentencias(texto: str) -> list[str]:
    """Los UPDATE del script, comparables: espacios unificados y números sin comillas con punto."""
    resultado = []
    for linea in texto.splitlines():
        linea = " ".join(linea.split())
        if linea.upper().startswith("UPDATE "):
            resultado.append(
                _NUMERO_ENTRE_COMILLAS.sub(
                    lambda m: str(Decimal(m.group(1).replace(",", "."))), linea
                )
            )
    return resultado


def original(nombre: str) -> str:
    return (CASO / "original" / nombre).read_text(encoding="cp1252")
