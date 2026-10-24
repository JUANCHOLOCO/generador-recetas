"""Contrato genérico para mantener tablas de parametrización desde la interfaz."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from recetas.core.domain.errors import RecetasError


@dataclass(frozen=True, slots=True)
class ColumnaEditable:
    nombre: str
    titulo: str
    opciones: tuple[str, ...] = ()  # valores permitidos (enums y S/N); vacío = texto libre
    ayuda: str = ""


@dataclass(frozen=True, slots=True)
class FilaParametro:
    id: int | None  # None = fila nueva
    valores: dict[str, str]  # todo como texto, tal como se ve en la tabla


@dataclass(frozen=True, slots=True)
class ErrorCelda:
    mensaje: str
    fila: int | None = None
    columna: str | None = None


@dataclass(frozen=True, slots=True)
class CambiosGuardados:
    insertadas: int = 0
    modificadas: int = 0
    eliminadas: int = 0


class ParametrizacionInvalidaError(RecetasError):
    def __init__(self, errores: Sequence[ErrorCelda]) -> None:
        super().__init__("; ".join(e.mensaje for e in errores))
        self.errores = list(errores)


class TablaMantenible(Protocol):
    @property
    def titulo(self) -> str: ...

    def columnas(self) -> tuple[ColumnaEditable, ...]: ...

    def listar(self) -> list[FilaParametro]: ...

    def guardar(self, filas: Sequence[FilaParametro]) -> CambiosGuardados:
        """Deja la tabla exactamente como `filas`: inserta, modifica y elimina en una transacción."""
        ...