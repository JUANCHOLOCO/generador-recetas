"""Tipo de facturación de una receta."""

from __future__ import annotations

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


class BillingScope(StrEnum):
    """A qué tipo de facturación aplica un dato de parametrización."""

    CORRIENTE = "CORRIENTE"
    ANTICIPADA = "ANTICIPADA"
    AMBAS = "AMBAS"

    def applies_to(self, billing: BillingType) -> bool:
        return self is BillingScope.AMBAS or self.value == billing.value

    @classmethod
    def for_billing(cls, billing: BillingType) -> tuple[BillingScope, BillingScope]:
        """Valores a incluir al consultar la parametrización de un tipo de facturación."""
        return (cls(billing.value), cls.AMBAS)
