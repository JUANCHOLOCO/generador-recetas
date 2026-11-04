"""Solicitudes de alza (planes pospago y paquetes): lo que el usuario ingresó, ya validado."""

from collections import Counter
from collections.abc import Iterable
from typing import Annotated, Self

from pydantic import AfterValidator, BaseModel, ConfigDict, model_validator
from pydantic_core import PydanticCustomError

from recetas.core.domain.ambiente import Ambiente
from recetas.modules.alza_tarifas.domain.valores import (
    Autor,
    IdNumerico,
    Nombre,
    PartNumPaquete,
    PartNumPlan,
    Precio,
    Requerimiento,
)


class _Inmutable(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class PlanAlza(_Inmutable):
    id: IdNumerico
    part_num: PartNumPlan
    nombre: Nombre
    precio_nuevo: Precio
    prorrateo_nuevo: Precio
    precio_actual: Precio
    prorrateo_actual: Precio


class PaqueteAlza(_Inmutable):
    id: IdNumerico
    part_num: PartNumPaquete
    nombre: Nombre
    con_iva_nuevo: Precio  # SERVICES.ITEM_PRICE y ATP_CORP_PRECIOS_SERVICE.ITEM_PRICE_IVA
    sin_iva_nuevo: Precio  # ATP_CORP_PRECIOS_SERVICE.ITEM_PRICE
    con_iva_actual: Precio
    sin_iva_actual: Precio


def _al_menos_un_plan(planes: tuple[PlanAlza, ...]) -> tuple[PlanAlza, ...]:
    if not planes:
        raise PydanticCustomError("sin_planes", "Debe agregar al menos un plan.")
    return planes


def _al_menos_un_paquete(paquetes: tuple[PaqueteAlza, ...]) -> tuple[PaqueteAlza, ...]:
    if not paquetes:
        raise PydanticCustomError("sin_paquetes", "Debe agregar al menos un paquete.")
    return paquetes


class _CabeceraAlza(_Inmutable):
    requerimiento: Requerimiento
    autor: Autor
    ambiente: Ambiente


class SolicitudAlzaPlanes(_CabeceraAlza):
    planes: Annotated[tuple[PlanAlza, ...], AfterValidator(_al_menos_un_plan)]

    @model_validator(mode="after")
    def _sin_duplicados(self) -> Self:
        _sin_repetidos(self.planes)
        return self


class SolicitudAlzaPaquetes(_CabeceraAlza):
    paquetes: Annotated[tuple[PaqueteAlza, ...], AfterValidator(_al_menos_un_paquete)]

    @model_validator(mode="after")
    def _sin_duplicados(self) -> Self:
        _sin_repetidos(self.paquetes)
        return self


def _sin_repetidos(filas: tuple[PlanAlza, ...] | tuple[PaqueteAlza, ...]) -> None:
    problemas = [
        *_repetidos("Id", (f.id for f in filas)),
        *_repetidos("Part_num", (f.part_num for f in filas)),
    ]
    if problemas:
        raise PydanticCustomError("duplicados", "{detalle}", {"detalle": " ".join(problemas)})


def _repetidos(campo: str, valores: Iterable[str]) -> list[str]:
    return [f"{campo} repetido: {valor}." for valor, veces in Counter(valores).items() if veces > 1]
