"""Tipos del dominio Pospago."""

from enum import StrEnum


class TipoPaquete(StrEnum):
    PLAN = "PLAN"
    DATA = "DATA"
    SMS = "SMS"


class ListaCambioPlan(StrEnum):
    """Listas de la matriz CPL_PLAN_PLAN, en el orden en que salen en el script."""

    PREPAGO = "PREPAGO"
    NINTENDO = "NINTENDO"
    ATP = "ATP"
    CONTROL = "CONTROL"
