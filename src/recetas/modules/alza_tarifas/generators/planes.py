"""Generador del alza de planes pospago (ACTIVATOR.PLANS)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self

from recetas.core.application.ports import TemplateRenderer
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.domain.sql import sql_literal
from recetas.modules.alza_tarifas.domain.solicitud import PlanAlza, SolicitudAlzaPlanes
from recetas.modules.alza_tarifas.domain.valores import sql_numero
from recetas.modules.alza_tarifas.generators.comun import ArmadorDeAlza, TipoAlza

PLANES = TipoAlza(
    carpeta="AlzaPlanesPospago",
    sufijo="PLANES_POSPAGO",
    descripcion="planes pospago",
    plantilla="alza_planes.sql.j2",
)


@dataclass(frozen=True, slots=True)
class FilaPlan:
    """Un plan ya formateado como SQL, listo para la plantilla."""

    nombre: str
    id: str
    part_num: str
    precio: str
    prorrateo: str

    @classmethod
    def crear(cls, plan: PlanAlza, precio: Decimal, prorrateo: Decimal) -> Self:
        return cls(
            nombre=plan.nombre,
            id=sql_literal(plan.id),
            part_num=sql_literal(plan.part_num),
            precio=sql_numero(precio),
            prorrateo=sql_numero(prorrateo),
        )


class AlzaPlanesGenerator:
    def __init__(self, renderer: TemplateRenderer) -> None:
        self._armador = ArmadorDeAlza(renderer, PLANES)

    def generar(
        self, solicitud: SolicitudAlzaPlanes, fecha: date, version: str, bundle: RecipeBundle
    ) -> None:
        planes = solicitud.planes
        self._armador.armar(
            bundle,
            requerimiento=solicitud.requerimiento,
            autor=solicitud.autor,
            fecha=fecha,
            version=version,
            nuevas=[FilaPlan.crear(p, p.precio_nuevo, p.prorrateo_nuevo) for p in planes],
            actuales=[FilaPlan.crear(p, p.precio_actual, p.prorrateo_actual) for p in planes],
        )
