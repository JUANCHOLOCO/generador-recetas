"""Reglas de texto compartidas por todos los módulos."""

import re

_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


def tiene_caracteres_de_control(texto: str) -> bool:
    """True si el texto contiene saltos de línea, tabuladores u otros caracteres de control.

    En un script de SQL*Plus, un salto de línea dentro de un literal parte la sentencia, y
    líneas como '/' o '@archivo' se interpretan como comandos aunque estén dentro de un texto.
    """
    return bool(_CONTROL.search(texto))
