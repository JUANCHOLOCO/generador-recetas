"""Reglas de texto compartidas por todos los módulos."""

import re

_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


def tiene_caracteres_de_control(texto: str) -> bool:
    """True si el texto contiene saltos de línea, tabuladores u otros caracteres de control.

    En un script de SQL*Plus, un salto de línea dentro de un literal parte la sentencia, y
    líneas como '/' o '@archivo' se interpretan como comandos aunque estén dentro de un texto.
    """
    return bool(_CONTROL.search(texto))


def caracteres_fuera_de_cp1252(texto: str) -> str:
    """Caracteres que no se pueden escribir en un script Windows-1252, listos para un mensaje.

    Devuelve "" si todos caben. Incluye el código Unicode porque algunos son invisibles
    (por ejemplo, el espacio de ancho cero U+200B que llega al copiar desde Teams o la web).
    """
    fuera: list[str] = []
    for caracter in texto:
        if caracter in fuera:
            continue
        try:
            caracter.encode("cp1252")
        except UnicodeEncodeError:
            fuera.append(caracter)
    return ", ".join(f"'{c}' (U+{ord(c):04X})" for c in fuera)
