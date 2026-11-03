from decimal import Decimal

import pytest
from pydantic import ValidationError

from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPlanes
from tests.factories import crear_solicitud_alza, datos_plan_alza


def test_solicitud_valida_conserva_los_valores_tal_cual() -> None:
    plan = crear_solicitud_alza().planes[0]

    assert plan.precio_nuevo == Decimal("68083")
    assert plan.prorrateo_actual == Decimal("51246.3")


def test_sin_planes_falla() -> None:
    with pytest.raises(ValidationError, match="al menos un plan"):
        SolicitudAlzaPlanes.model_validate(
            {"requerimiento": "TPFB-1726", "autor": "jbotero", "ambiente": "PROD", "planes": []}
        )


def test_part_num_repetido_falla() -> None:
    with pytest.raises(ValidationError, match="Part_num repetido: PLCON0335"):
        crear_solicitud_alza(datos_plan_alza(), datos_plan_alza(id="1209"))


def test_part_num_de_paquete_no_sirve_para_un_plan() -> None:
    with pytest.raises(ValidationError, match="PLCON####"):
        crear_solicitud_alza(datos_plan_alza(part_num="SVALL2322"))
