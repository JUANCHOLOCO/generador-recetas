"""Tipo de facturación de una receta."""

from enum import StrEnum
from typing import assert_never


class BillingType(StrEnum):
    CORRIENTE = "CORRIENTE"
    ANTICIPADA = "ANTICIPADA"

    @property
    def label(self) -> str:
        """Texto para mostrar en la interfaz."""
        match self:
            case BillingType.CORRIENTE:
                return "Corriente (FC)"
            case BillingType.ANTICIPADA:
                return "Anticipada"
            case _:
                assert_never(self)
