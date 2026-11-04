"""Generador del alza de planes pospago: aplica, rollback y lanzadores en ACTIVATOR."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self

from recetas.core.application.ports import TemplateRenderer
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.domain.scripts import CabeceraScript
from recetas.core.domain.sql import sql_literal
from recetas.modules.alza_tarifas.domain.solicitud import PlanAlza, SolicitudAlzaPlanes
from recetas.modules.alza_tarifas.domain.valores import sql_numero

ESQUEMA = "ACTIVATOR"
CARPETA = "AlzaPlanesPospago"  # carpeta propia: no choca con el alza de paquetes del mismo RQ


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
        self._renderer = renderer

    def generar(
        self, solicitud: SolicitudAlzaPlanes, fecha: date, version: str, bundle: RecipeBundle
    ) -> None:
        rq = solicitud.requerimiento
        base = f"{CARPETA}/Script/ACTIVADOR"
        script = f"1_UPDATE_{rq}_PLANES_POSPAGO_SCRIPT.SQL"
        rollback = f"1_ROLLBACK_UPDATE_{rq}_PLANES_POSPAGO_SCRIPT.SQL"

        def cabecera(objetivo: str) -> CabeceraScript:
            return CabeceraScript(
                requerimiento=rq,
                objetivo=objetivo,
                base_datos=ESQUEMA,
                autor=solicitud.autor,
                fecha=fecha,
                version=version,
            )

        cab_aplica = cabecera("Alza de tarifas de planes pospago")
        cab_rollback = cabecera("Rollback del alza de tarifas de planes pospago")
        nuevos = [FilaPlan.crear(p, p.precio_nuevo, p.prorrateo_nuevo) for p in solicitud.planes]
        actuales = [
            FilaPlan.crear(p, p.precio_actual, p.prorrateo_actual) for p in solicitud.planes
        ]

        bundle.add(f"{base}/aplica-cambio.sql", self._lanzador(cab_aplica, f"SQL/{script}"))
        bundle.add(
            f"{base}/rollback-cambio.sql", self._lanzador(cab_rollback, f"ROLLBACK/{rollback}")
        )
        bundle.add(f"{base}/SQL/{script}", self._script(cab_aplica, nuevos))
        bundle.add(f"{base}/ROLLBACK/{rollback}", self._script(cab_rollback, actuales))

    def _lanzador(self, cab: CabeceraScript, script: str) -> str:
        return self._renderer.render("wrapper.sql.j2", cab=cab, esquema=ESQUEMA, script=script)

    def _script(self, cab: CabeceraScript, planes: list[FilaPlan]) -> str:
        return self._renderer.render("alza_planes.sql.j2", cab=cab, planes=planes)
