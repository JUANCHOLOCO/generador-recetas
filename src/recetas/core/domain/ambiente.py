"""Ambiente de destino de la receta."""

from enum import StrEnum
from typing import assert_never


class Ambiente(StrEnum):
    DEV = "DEV"
    UAT = "UAT"
    PROD = "PROD"

    @property
    def sufijo(self) -> str:
        """Sufijo de la carpeta raíz de la receta (ej. TPFB-2753_Prod)."""
        match self:
            case Ambiente.DEV:
                return "Dev"
            case Ambiente.UAT:
                return "UAT"
            case Ambiente.PROD:
                return "Prod"
            case _:
                assert_never(self)
