"""Generador ACTIVATOR: alta de planes, servicios, matriz de cambios, roles y scoring."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from recetas.core.domain.scripts import CabeceraScript
from recetas.core.domain.sql import es_literal_sql, sql_literal
from recetas.modules.creacion_planes_pospago.domain.errors import ParametrizacionIncompletaError
from recetas.modules.creacion_planes_pospago.domain.matriz import (
    SeccionMatriz,
    matriz_cambio_plan,
)
from recetas.modules.creacion_planes_pospago.domain.plan import PlanNuevo
from recetas.modules.creacion_planes_pospago.domain.tipos import TipoPaquete
from recetas.modules.creacion_planes_pospago.generators.base import (
    BaseSqlGenerator,
    ContextoGeneracion,
)

# Columnas en el orden exacto de los scripts de ejemplo.
COLUMNAS_PLANS = (
    "ID", "PART_NUM", "NAME", "DESCRIPTION", "SUBSCRIPTION_TYPE", "TARIFF_GROUP_ID",
    "ITEM_PRICE", "ITEM_PRICE_PRORRATE", "STATUS", "ID_XML", "VENDOR_VALUE", "SPID",
    "ADVANCED_CBM", "ID_RETENTION", "RETENTION_VALUE", "EVIDENTE_REQUIRED", "MAX_LINES_MASIVE",
    "MAX_LINES_CORPORATE", "VALIDATE_SCORE", "TYPE", "BENEFIT", "BILLING_TYPE", "CESION_STATUS",
    "RTB", "MANAGER_CB", "PART_NUM_PKG", "PART_NUM_DESCRIPTION", "PRODUCT_DESCRIPTION",
    "CONSUMPTION_LIMIT", "FIXED_CHARGED_CBA", "REVENUE", "SELECCIONCICLOFACTURACION",
    "CONSULT_SCORE",
)  # fmt: skip
COLUMNAS_SERVICES = (
    "ID", "TYPE", "SUBTYPE", "CATEGORY", "ATTRIBUTE", "PRIORITY", "PART_NUM", "PART_NUM_DESC",
    "DESCRIPTION", "STATUS", "XML", "NET_PARAMETERS", "ITEM_PRICE", "APP_FACTOR", "DEPENDENCE",
    "REVENUE", "BILLING_TYPE", "PCRF_CODE", "PCRF_PROMOTION", "PCRF_PERIOD_MONTH",
)  # fmt: skip
COLUMNAS_PLAN_SERVICE = (
    "ID_PLAN", "ID_SERVICE", "IS_DEFAULT", "SHOW_SERVICE", "AMOUNT",
    "SHOW_SERVICE_POSTSALE", "RETENTION", "PROFILES",
)  # fmt: skip


@dataclass(frozen=True, slots=True)
class PlanActivador:
    """Datos de un plan ya formateados como SQL, listos para la plantilla."""

    id_plan: str
    nombre: str
    svall_datos: str
    codigo_pcrf: str
    pcrf_code: str
    plans: tuple[str, ...]
    services_datos: tuple[str, ...]
    services_sms: tuple[str, ...]
    plan_services: tuple[tuple[str, ...], ...]
    matriz: tuple[SeccionMatriz, ...]


def valores_fila(
    tabla: str,
    columnas: Sequence[str],
    dinamicos: Mapping[str, str],
    estaticos: Mapping[str, str],
) -> tuple[str, ...]:
    """Valor SQL de cada columna: primero el del formulario, si no, el de la parametrización."""
    faltantes = [c for c in columnas if c not in dinamicos and c not in estaticos]
    if faltantes:
        raise ParametrizacionIncompletaError(
            f"Faltan campos estáticos de {tabla}: {', '.join(faltantes)}."
        )
    invalidos = [c for c in columnas if c not in dinamicos and not es_literal_sql(estaticos[c])]
    if invalidos:
        detalle = ", ".join(f"{c} = {estaticos[c]!r}" for c in invalidos)
        raise ParametrizacionIncompletaError(
            f"Valores estáticos inválidos en {tabla}: {detalle}. "
            "Use null, un número o un texto entre comillas simples."
        )
    return tuple(dinamicos[c] if c in dinamicos else estaticos[c] for c in columnas)


def subconsulta_servicio(svall: str) -> str:
    return f"(SELECT S.ID FROM ACTIVATOR.SERVICES S WHERE S.PART_NUM = {sql_literal(svall)})"


class ActivadorGenerator(BaseSqlGenerator):
    esquema = "ACTIVATOR"
    carpeta = "ACTIVADOR"
    objetivo_aplica = "Insercion de nuevos planes"
    objetivo_rollback = "Rollback de la insercion de nuevos planes"

    def nombre_script(self, rq: str) -> str:
        return f"1_INSERT_{rq}_SCRIPT.SQL"

    def nombre_rollback(self, rq: str) -> str:
        return f"1_ROLLBACK_INSERT_{rq}_SCRIPT.SQL"

    def contenido_script(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        p = ctx.parametrizacion
        ids_nuevos = [plan.id_plan for plan in ctx.solicitud.planes]
        return self._renderer.render(
            "activador_aplica.sql.j2",
            cab=cab,
            columnas={
                "plans": COLUMNAS_PLANS,
                "services": COLUMNAS_SERVICES,
                "plan_service": COLUMNAS_PLAN_SERVICE,
            },
            planes=[self._plan(plan, ctx, ids_nuevos) for plan in ctx.solicitud.planes],
            roles=p.roles,
            scoring_plan=p.scoring_plan,
            cpl_scoring_plan=p.cpl_scoring_plan,
            canales=p.canales,
            ids_planes=ids_nuevos,
        )

    def contenido_rollback(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        planes = ctx.solicitud.planes
        svalls = [s for plan in planes for s in (plan.datos.svall, plan.sms.svall)]
        return self._renderer.render(
            "activador_rollback.sql.j2",
            cab=cab,
            ids_planes=[plan.id_plan for plan in planes],
            svalls_nuevos=svalls,
            svalls_y_addons=[*svalls, *ctx.parametrizacion.addons],
        )

    def _plan(
        self, plan: PlanNuevo, ctx: ContextoGeneracion, ids_nuevos: Sequence[str]
    ) -> PlanActivador:
        p = ctx.parametrizacion
        texto = sql_literal
        plans = valores_fila(
            "PLANS",
            COLUMNAS_PLANS,
            {
                "ID": texto(plan.id_plan),
                "PART_NUM": texto(plan.part_num),
                "NAME": texto(plan.nombre),
                "DESCRIPTION": texto(plan.nombre),
                "TARIFF_GROUP_ID": texto(plan.tarif_group),
                "ITEM_PRICE": texto(plan.valor_con_iva),
                "ITEM_PRICE_PRORRATE": texto(plan.valor_sin_iva),
                "VENDOR_VALUE": texto(plan.valor_con_iva),
                "BILLING_TYPE": texto(ctx.estrategia.billing_type_plans),
                "PRODUCT_DESCRIPTION": texto(plan.nombre),
            },
            p.valores("PLANS", TipoPaquete.PLAN),
        )
        services_datos = valores_fila(
            "SERVICES (datos)",
            COLUMNAS_SERVICES,
            {
                "PART_NUM": texto(plan.datos.svall),
                "PART_NUM_DESC": texto(plan.datos.nombre),
                "DESCRIPTION": texto(plan.datos.nombre),
                "PCRF_CODE": texto(plan.pcrf_code),
            },
            p.valores("SERVICES", TipoPaquete.DATA),
        )
        services_sms = valores_fila(
            "SERVICES (SMS)",
            COLUMNAS_SERVICES,
            {
                "TYPE": "'SMS'",
                "SUBTYPE": "'SMS'",
                "PART_NUM": texto(plan.sms.svall),
                "PART_NUM_DESC": texto(plan.sms.nombre),
                "DESCRIPTION": texto(plan.sms.nombre),
            },
            p.valores("SERVICES", TipoPaquete.SMS),
        )
        ps_datos = p.valores("PLAN_SERVICE", TipoPaquete.DATA)
        ps_sms = p.valores("PLAN_SERVICE", TipoPaquete.SMS)
        id_plan = texto(plan.id_plan)
        plan_services = (
            valores_fila(
                "PLAN_SERVICE (datos)",
                COLUMNAS_PLAN_SERVICE,
                {"ID_PLAN": id_plan, "ID_SERVICE": subconsulta_servicio(plan.datos.svall)},
                ps_datos,
            ),
            valores_fila(
                "PLAN_SERVICE (SMS)",
                COLUMNAS_PLAN_SERVICE,
                {"ID_PLAN": id_plan, "ID_SERVICE": subconsulta_servicio(plan.sms.svall)},
                ps_sms,
            ),
            *(
                valores_fila(
                    "PLAN_SERVICE (add-on)",
                    COLUMNAS_PLAN_SERVICE,
                    {
                        "ID_PLAN": id_plan,
                        "ID_SERVICE": subconsulta_servicio(addon),
                        "IS_DEFAULT": "'0'",
                    },
                    ps_datos,
                )
                for addon in p.addons
            ),
        )
        return PlanActivador(
            id_plan=plan.id_plan,
            nombre=plan.nombre,
            svall_datos=plan.datos.svall,
            codigo_pcrf=plan.codigo_pcrf,
            pcrf_code=plan.pcrf_code,
            plans=plans,
            services_datos=services_datos,
            services_sms=services_sms,
            plan_services=plan_services,
            matriz=matriz_cambio_plan(plan.id_plan, ids_nuevos, p),
        )
