"""Entidades del formulario: los planes nuevos que el usuario quiere crear."""

from collections import Counter
from collections.abc import Iterable
from typing import Annotated, Self

from pydantic import AfterValidator, BaseModel, ConfigDict, model_validator
from pydantic_core import PydanticCustomError

from recetas.core.domain.ambiente import Ambiente
from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.valores import (
    Autor,
    CodigoPcrf,
    IdPlan,
    Nombre,
    PartNum,
    Poid,
    Requerimiento,
    Svall,
    TarifGroup,
    Valor,
    NombrePlan,
)


class _Inmutable(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Paquete(_Inmutable):
    nombre: Nombre
    svall: Svall
    poid: Poid


class PlanNuevo(_Inmutable):
    id_plan: IdPlan
    part_num: PartNum
    nombre: NombrePlan
    valor_con_iva: Valor
    valor_sin_iva: Valor
    codigo_pcrf: CodigoPcrf
    tarif_group: TarifGroup
    es_53: bool = False
    datos: Paquete
    sms: Paquete

    @property
    def poid_plan(self) -> str:
        """El POID del plan coincide siempre con su tarif group."""
        return self.tarif_group

    @property
    def pcrf_code(self) -> str:
        return f"MONTH/{self.codigo_pcrf}"

    @model_validator(mode="after")
    def _sin_iva_menor_que_con_iva(self) -> Self:
        if self.valor_sin_iva >= self.valor_con_iva:
            raise PydanticCustomError(
                "valor_sin_iva", "El valor sin IVA debe ser menor que el valor con IVA."
            )
        return self


def _al_menos_un_plan(planes: tuple[PlanNuevo, ...]) -> tuple[PlanNuevo, ...]:
    if not planes:
        raise PydanticCustomError("sin_planes", "Debe agregar al menos un plan.")
    return planes


class SolicitudReceta(_Inmutable):
    requerimiento: Requerimiento
    autor: Autor
    ambiente: Ambiente
    tipo: BillingType
    planes: Annotated[tuple[PlanNuevo, ...], AfterValidator(_al_menos_un_plan)]

    @model_validator(mode="after")
    def _sin_duplicados(self) -> Self:
        problemas = [
            *_repetidos("Id_Plan", (p.id_plan for p in self.planes)),
            *_repetidos("Part_num", (p.part_num for p in self.planes)),
            *_repetidos("Svall", (s for p in self.planes for s in (p.datos.svall, p.sms.svall))),
        ]
        if problemas:
            raise PydanticCustomError("duplicados", "{detalle}", {"detalle": " ".join(problemas)})
        return self


def _repetidos(campo: str, valores: Iterable[str]) -> list[str]:
    return [f"{campo} repetido: {valor}." for valor, veces in Counter(valores).items() if veces > 1]
