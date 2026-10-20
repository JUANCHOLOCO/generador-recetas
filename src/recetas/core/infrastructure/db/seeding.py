"""Carga de datos iniciales (seeds) desde CSV hacia tablas vacías."""

import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.orm import Session

from recetas.core.infrastructure.db.base import Base

_VERDADEROS = {"1", "true", "si", "sí"}


def leer_csv[M: Base](ruta: Path, model: type[M]) -> Iterator[M]:
    """Crea una instancia del modelo por fila, convirtiendo cada valor al tipo de su columna."""
    columnas = model.__table__.columns
    with ruta.open(encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        desconocidas = set(lector.fieldnames or ()) - set(columnas.keys())
        if desconocidas:
            raise ValueError(f"{ruta.name}: columnas desconocidas {sorted(desconocidas)}")
        for fila in lector:
            yield model(**{nombre: _convertir(columnas[nombre], v) for nombre, v in fila.items()})


def seed_if_empty(session: Session, model: type[Base], ruta: Path) -> int:
    """Inserta el CSV solo si la tabla está vacía. Devuelve cuántas filas insertó."""
    if session.scalar(select(func.count()).select_from(model)):
        return 0
    filas = list(leer_csv(ruta, model))
    session.add_all(filas)
    return len(filas)


def _convertir(columna: ColumnElement[Any], valor: str) -> object:
    if valor == "":
        return None
    tipo = columna.type.python_type
    if tipo is bool:
        return valor.strip().lower() in _VERDADEROS
    return tipo(valor)
