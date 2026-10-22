"""Generador PROMOTIONS: identificación de POIDs y variables de promociones."""

from dataclasses import dataclass

from recetas.core.domain.scripts import CabeceraScript
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion
from recetas.modules.creacion_planes_pospago.domain.plan import PlanNuevo
from recetas.modules.creacion_planes_pospago.domain.tipos import TipoPaquete
from recetas.modules.creacion_planes_pospago.generators.base import (
    BaseSqlGenerator,
    ContextoGeneracion,
)

# Fila PLAN_TYPE de la familia en TBL_PROM_VARIABLES (fija también en la macro).
FAMILIA_PLAN_TYPE = "POSPAGO5"


@dataclass(frozen=True, slots=True)
class FilaPoid:
    nombre: str
    poid: str
    identify: str
    descripcion: str


def filas_poid(plan: PlanNuevo, parametrizacion: Parametrizacion) -> tuple[FilaPoid, ...]:
    """Las 3 filas de un plan, en el orden de los ejemplos: plan, SMS, datos."""
    return (
        FilaPoid(
            plan.nombre,
            plan.poid_plan,
            parametrizacion.identify_de(TipoPaquete.PLAN),
            f"Descuento {plan.nombre} telefonia",
        ),
        FilaPoid(
            plan.sms.nombre,
            plan.sms.poid,
            parametrizacion.identify_de(TipoPaquete.SMS),
            f"Descuento {plan.nombre} sms",
        ),
        FilaPoid(
            plan.datos.nombre,
            plan.datos.poid,
            parametrizacion.identify_de(TipoPaquete.DATA),
            f"Descuento {plan.nombre} datos",
        ),
    )


class PromotionsGenerator(BaseSqlGenerator):
    esquema = "PROMOTIONS"
    carpeta = "PROMOTIONS"
    objetivo_aplica = "Insercion de los nuevos planes en promociones"
    objetivo_rollback = "Rollback de los nuevos planes en promociones"

    def nombre_script(self, rq: str) -> str:
        return f"1_POID_IDENTIFY_{rq}.SQL"

    def nombre_rollback(self, rq: str) -> str:
        return f"1_PROMOTIONS_ROLLBACK_{rq}.SQL"

    def contenido_script(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        return self._renderer.render(
            "promotions_aplica.sql.j2",
            cab=cab,
            planes=ctx.solicitud.planes,
            filas=[f for p in ctx.solicitud.planes for f in filas_poid(p, ctx.parametrizacion)],
            familia=FAMILIA_PLAN_TYPE,
        )

    def contenido_rollback(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        return self._renderer.render(
            "promotions_rollback.sql.j2", cab=cab, planes=ctx.solicitud.planes
        )
