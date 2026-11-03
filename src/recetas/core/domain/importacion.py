"""Tablas importadas (Excel): encabezados esperados y celdas convertidas a texto."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from recetas.core.domain.errors import ImportacionError


@dataclass(frozen=True, slots=True)
class FormatoHoja:
    """Cómo viene la tabla en el archivo. Cada módulo declara el suyo."""

    encabezados: tuple[str, ...]
    fila_encabezado: int = 1  # numerada como en Excel: la primera fila es la 1


def a_texto(valor: object) -> str:
    """Celda de Excel como texto: vacía → "", 19900.0 → "19900"."""
    if valor is None:
        return ""
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor).strip()


def letra_columna(indice: int) -> str:
    """0 → A, 25 → Z, 26 → AA (como Excel)."""
    letras = ""
    numero = indice + 1
    while numero:
        numero, resto = divmod(numero - 1, 26)
        letras = chr(ord("A") + resto) + letras
    return letras


def extraer_filas(celdas: Iterable[Sequence[object]], formato: FormatoHoja) -> list[list[str]]:
    """Valida los encabezados y devuelve las filas de datos (sin las vacías) como texto."""
    filas = [[a_texto(valor) for valor in fila] for fila in celdas]
    if len(filas) < formato.fila_encabezado:
        raise ImportacionError(
            f"El archivo no tiene la fila de encabezados (fila {formato.fila_encabezado})."
        )

    encabezado = filas[formato.fila_encabezado - 1]
    for i, esperado in enumerate(formato.encabezados):
        actual = encabezado[i] if i < len(encabezado) else ""
        if _normalizar(actual) != _normalizar(esperado):
            celda = f"{letra_columna(i)}{formato.fila_encabezado}"
            raise ImportacionError(
                f"El archivo no tiene el formato esperado: la celda {celda} debe decir "
                f"'{esperado}' y dice '{actual}'."
            )

    ancho = len(formato.encabezados)
    datos: list[list[str]] = []
    for fila in filas[formato.fila_encabezado :]:
        valores = (fila + [""] * ancho)[:ancho]  # completa las filas cortas y corta columnas extra
        if any(valores):
            datos.append(valores)
    return datos


def _normalizar(texto: str) -> str:
    return " ".join(texto.split()).casefold()
