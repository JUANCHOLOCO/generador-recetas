"""Datos comunes de los scripts generados."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class CabeceraScript:
    requerimiento: str
    objetivo: str
    base_datos: str
    autor: str
    fecha: date
    version: str

    @property
    def fecha_texto(self) -> str:
        return self.fecha.strftime("%d/%m/%Y")