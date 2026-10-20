"""Constructores de objetos de dominio con valores por defecto para los tests."""

from collections.abc import Sequence
from dataclasses import replace
from typing import Any

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion
from recetas.modules.creacion_planes_pospago.domain.plan import PlanNuevo, SolicitudReceta


def crear_parametrizacion(**cambios: Any) -> Parametrizacion:
    base = Parametrizacion(
        tipo=BillingType.CORRIENTE,
        ids_cambio_plan=(),
        scoring_plan=(),
        cpl_scoring_plan=(),
        canales=(),
        campos_estaticos=(),
        cadena_pool=(),
        planes_53=(),
        identify={},
        roles=(),
        addons=(),
    )
    return replace(base, **cambios)


def datos_plan(**cambios: Any) -> dict[str, Any]:
    """Datos del plan 'Pospago Conectados 5.1 FC' de TPFB-2753 (Corriente)."""
    datos: dict[str, Any] = {
        "id_plan": "7751",
        "part_num": "PLCON0454",
        "nombre": "Pospago Conectados 5.1 FC",
        "valor_con_iva": 19900,
        "valor_sin_iva": 16723,
        "codigo_pcrf": "Conectados_51_FC",
        "tarif_group": "120617",
        "es_53": False,
        "datos": {
            "nombre": "Paquete Conectados Datos 5.1 FC",
            "svall": "SVALL2632",
            "poid": "990000885",
        },
        "sms": {
            "nombre": "Paquete Conectados SMS 5.1 FC",
            "svall": "SVALL2640",
            "poid": "990001008",
        },
    }
    return datos | cambios


def crear_plan(**cambios: Any) -> PlanNuevo:
    return PlanNuevo.model_validate(datos_plan(**cambios))


def crear_solicitud(
    planes: Sequence[dict[str, Any]] | None = None, **cambios: Any
) -> SolicitudReceta:
    datos: dict[str, Any] = {
        "requerimiento": "TPFB-2753",
        "tipo": "CORRIENTE",
        "planes": list(planes) if planes is not None else [datos_plan()],
    }
    return SolicitudReceta.model_validate(datos | cambios)
