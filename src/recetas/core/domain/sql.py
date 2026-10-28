"""Formato de literales SQL (Oracle)."""

import re

_LITERAL_SQL = re.compile(r"null|-?\d+(\.\d+)?|'(?:[^']|'')*'", re.IGNORECASE)


def es_literal_sql(valor: str) -> bool:
    """True si el valor es exactamente un literal: null, un número o un texto entre comillas."""
    return bool(_LITERAL_SQL.fullmatch(valor.strip()))


def sql_literal(valor: object) -> str:
    """Literal SQL seguro: comillas simples escapadas; None se convierte en NULL."""
    if valor is None:
        return "NULL"
    return "'" + str(valor).replace("'", "''") + "'"
