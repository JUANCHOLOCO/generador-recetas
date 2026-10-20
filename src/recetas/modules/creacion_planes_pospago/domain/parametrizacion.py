"""Parametrización del módulo: lo que antes era la hoja 'Reglas Aplicabilidad'."""

from collections.abc import Mapping
from dataclasses import dataclass

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.errors import ParametrizacionIncompletaError
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan, TipoPaquete


@dataclass(frozen=True, slots=True)
class IdCambioPlan:
    id_plan: str
    lista: ListaCambioPlan


@dataclass(frozen=True, slots=True)
class CampoEstatico:
    tabla: str
    tipo_paquete: TipoPaquete
    columna: str
    valor_sql: str


@dataclass(frozen=True, slots=True)
class Plan53:
    id_plan: str
    part_num: str


@dataclass(frozen=True, slots=True)
class Parametrizacion:
    """Foto de la parametrización vigente para un tipo de facturación."""

    tipo: BillingType
    ids_cambio_plan: tuple[IdCambioPlan, ...]
    scoring_plan: tuple[int, ...]
    cpl_scoring_plan: tuple[int, ...]
    canales: tuple[str, ...]
    campos_estaticos: tuple[CampoEstatico, ...]
    cadena_pool: tuple[str, ...]
    planes_53: tuple[Plan53, ...]
    identify: Mapping[TipoPaquete, str]
    roles: tuple[str, ...]
    addons: tuple[str, ...]

    def ids_de_lista(self, lista: ListaCambioPlan) -> tuple[str, ...]:
        return tuple(i.id_plan for i in self.ids_cambio_plan if i.lista is lista)

    def campos(self, tabla: str, tipo_paquete: TipoPaquete) -> tuple[CampoEstatico, ...]:
        return tuple(
            c
            for c in self.campos_estaticos
            if c.tabla == tabla and c.tipo_paquete is tipo_paquete
        )

    def identify_de(self, tipo_paquete: TipoPaquete) -> str:
        try:
            return self.identify[tipo_paquete]
        except KeyError:
            raise ParametrizacionIncompletaError(
                f"No hay IDENTIFY configurado para el tipo de paquete {tipo_paquete}."
            ) from None