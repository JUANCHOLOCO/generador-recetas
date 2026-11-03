"""Solicitud de alza de planes pospago: lo que el usuario ingresó, ya validado."""

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


def _al_menos_uno(planes: tuple[PlanAlza, ...]) -> tuple[PlanAlza, ...]:
    if not planes:
        raise PydanticCustomError("sin_planes", "Debe agregar al menos un plan.")
    return planes


class SolicitudAlzaPlanes(_Inmutable):
    requerimiento: Requerimiento
    autor: Autor
    ambiente: Ambiente
    planes: Annotated[tuple[PlanAlza, ...], AfterValidator(_al_menos_uno)]

    @model_validator(mode="after")
    def _sin_duplicados(self) -> Self:
        problemas = [
            *_repetidos("Id", (p.id for p in self.planes)),
            *_repetidos("Part_num", (p.part_num for p in self.planes)),
        ]
        if problemas:
            raise PydanticCustomError("duplicados", "{detalle}", {"detalle": " ".join(problemas)})
        return self


def _repetidos(campo: str, valores: Iterable[str]) -> list[str]:
    return [f"{campo} repetido: {valor}." for valor, veces in Counter(valores).items() if veces > 1]
