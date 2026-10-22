"""Generador SIEBEL: productos, atributos, POIDs, categorías de add-ons y lista de valores."""

from dataclasses import dataclass

from recetas.core.domain.scripts import CabeceraScript
from recetas.modules.creacion_planes_pospago.domain.matriz import ids_existentes
from recetas.modules.creacion_planes_pospago.domain.plan import PlanNuevo
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan
from recetas.modules.creacion_planes_pospago.generators.base import (
    BaseSqlGenerator,
    ContextoGeneracion,
)

# Valores fijos de la familia (también lo eran en la macro). Ver docs del módulo, sección 7.
POID_PROVISIONAL = "999999999"
IDS_CATEGORIA_ADDONS = (1, 2, 3)


@dataclass(frozen=True, slots=True)
class ProductoSiebel:
    nombre: str
    tipo: str
    part_num: str
    servicio: str
    poid: str
    uom_cd: str = ""
    prod_global_uid: str = ""
    prod_cls_num: str = ""
    attrib_04: str = ""

    @property
    def servicio_brm(self) -> str:
        return f"0.0.0.1 /service/cuentacontrol/{self.servicio}"

    def product(self, poid: str | None = None) -> str:
        return f"0.0.0.1 /product {poid or self.poid} 1"

    def deal(self, poid: str | None = None) -> str:
        return f"0.0.0.1 /deal {poid or self.poid} 0"


@dataclass(frozen=True, slots=True)
class PlanSiebel:
    plan: ProductoSiebel
    datos: ProductoSiebel
    sms: ProductoSiebel
    lista_de_valores: str

    @property
    def orden_alta(self) -> tuple[ProductoSiebel, ...]:
        """Orden de los ejemplos en S_PROD_INT y en el INSERT de S_PROD_INT_X."""
        return (self.plan, self.datos, self.sms)

    @property
    def orden_atributos(self) -> tuple[ProductoSiebel, ...]:
        """Orden de los ejemplos en la actualización completa de atributos."""
        return (self.plan, self.sms, self.datos)


def plan_siebel(plan: PlanNuevo, cadena_pool: tuple[str, ...]) -> PlanSiebel:
    return PlanSiebel(
        plan=ProductoSiebel(
            plan.nombre,
            "TELEFONIA_POS",
            plan.part_num,
            "telephony",
            plan.poid_plan,
            uom_cd="Por mes",
            prod_global_uid="11042",
            prod_cls_num="120",
            attrib_04="120354",
        ),
        datos=ProductoSiebel(plan.datos.nombre, "DATA", plan.datos.svall, "gprs", plan.datos.poid),
        sms=ProductoSiebel(plan.sms.nombre, "SMS", plan.sms.svall, "sms", plan.sms.poid),
        lista_de_valores="|".join((*cadena_pool, plan.datos.svall, plan.sms.svall, plan.part_num))
        + "|",
    )


def cancela_cp_planes(ids: list[str]) -> str:
    return "".join(f"[{i}]" for i in ids)


class SiebelGenerator(BaseSqlGenerator):
    esquema = "SIEBEL"
    carpeta = "SIEBEL"
    objetivo_aplica = "Actualizacion de los productos de los nuevos planes"
    objetivo_rollback = "Rollback de la actualizacion de los productos"

    def nombre_script(self, rq: str) -> str:
        return f"1_UPDATE_PRODUCTOS_{rq}_SCRIPT.SQL"

    def nombre_rollback(self, rq: str) -> str:
        return f"1_ROLLBACK_UPDATE_PRODUCTOS_{rq}_SCRIPT.SQL"

    def contenido_script(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        planes = self._planes(ctx)
        ids_nuevos = [p.id_plan for p in ctx.solicitud.planes]
        return self._renderer.render(
            "siebel_aplica.sql.j2",
            cab=cab,
            planes=planes,
            sincronizacion=[
                *(p.datos for p in planes),
                *(p.sms for p in planes),
                *(p.plan for p in planes),
            ],
            poid_provisional=POID_PROVISIONAL,
            ids_categoria=IDS_CATEGORIA_ADDONS,
            cancela=cancela_cp_planes([*self._nintendo_existentes(ctx), *ids_nuevos]),
        )

    def contenido_rollback(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        return self._renderer.render(
            "siebel_rollback.sql.j2",
            cab=cab,
            planes=self._planes(ctx),
            ids_categoria=IDS_CATEGORIA_ADDONS,
            cancela=cancela_cp_planes(self._nintendo_existentes(ctx)),
        )

    def _planes(self, ctx: ContextoGeneracion) -> list[PlanSiebel]:
        return [plan_siebel(p, ctx.parametrizacion.cadena_pool) for p in ctx.solicitud.planes]

    def _nintendo_existentes(self, ctx: ContextoGeneracion) -> list[str]:
        ids_nuevos = [p.id_plan for p in ctx.solicitud.planes]
        return ids_existentes(ListaCambioPlan.NINTENDO, ids_nuevos, ctx.parametrizacion)
