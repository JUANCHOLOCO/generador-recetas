"""Formato de literales SQL (Oracle)."""


def sql_literal(valor: object) -> str:
    """Literal SQL seguro: comillas simples escapadas; None se convierte en NULL."""
    if valor is None:
        return "NULL"
    return "'" + str(valor).replace("'", "''") + "'"
