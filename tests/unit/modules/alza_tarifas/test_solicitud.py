from decimal import Decimal

import pytest
from pydantic import ValidationError

from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPaquetes, SolicitudAlzaPlanes
from tests.factories import (
    crear_solicitud_alza,
    crear_solicitud_paquetes,
    datos_paquete_alza,
    datos_plan_alza,
)


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


def test_solicitud_de_paquetes_valida() -> None:
    paquete = crear_solicitud_paquetes().paquetes[0]

    assert paquete.con_iva_nuevo == Decimal("13990")
    assert paquete.sin_iva_actual == Decimal("10605.04")


def test_sin_paquetes_falla() -> None:
    with pytest.raises(ValidationError, match="al menos un paquete"):
        SolicitudAlzaPaquetes.model_validate(
            {"requerimiento": "TPFB-1726", "autor": "jbotero", "ambiente": "PROD", "paquetes": []}
        )


def test_part_num_de_plan_no_sirve_para_un_paquete() -> None:
    with pytest.raises(ValidationError, match="SVALL####"):
        crear_solicitud_paquetes(datos_paquete_alza(part_num="PLCON0335"))


def test_id_de_paquete_repetido_falla() -> None:
    with pytest.raises(ValidationError, match="Id repetido: 28708"):
        crear_solicitud_paquetes(datos_paquete_alza(), datos_paquete_alza(part_num="SVALL2323"))
