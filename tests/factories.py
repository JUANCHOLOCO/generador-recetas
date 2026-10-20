"""Constructores de objetos de dominio con valores por defecto para los tests."""

from dataclasses import replace
from typing import Any

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion


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
