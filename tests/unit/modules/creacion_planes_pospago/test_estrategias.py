import pytest

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.estrategias import (
    AnticipadaStrategy,
    CorrienteStrategy,
    estrategia_para,
)


@pytest.mark.parametrize(
    ("tipo", "billing_type", "carpeta", "rq"),
    [
        (BillingType.CORRIENTE, "Vencida", "Corriente", "TPFB-2753_CORRIENTE"),
        (BillingType.ANTICIPADA, "Anticipada", "Anticipados", "TPFB-2753"),
    ],
)
def test_valores_de_cada_estrategia(
    tipo: BillingType, billing_type: str, carpeta: str, rq: str
) -> None:
    estrategia = estrategia_para(tipo)

    assert estrategia.tipo is tipo
    assert estrategia.billing_type_plans == billing_type
    assert estrategia.carpeta == carpeta
    assert estrategia.rq_archivos("TPFB-2753") == rq


def test_factory_devuelve_la_clase_correcta() -> None:
    assert isinstance(estrategia_para(BillingType.CORRIENTE), CorrienteStrategy)
    assert isinstance(estrategia_para(BillingType.ANTICIPADA), AnticipadaStrategy)


def test_corriente_advierte_nombres_sin_fc() -> None:
    corriente = CorrienteStrategy()

    assert corriente.advertencia_nombre("Pospago Conectados 5.1 FC") is None
    assert "no termina en 'FC'" in (corriente.advertencia_nombre("Pospago Conectados 5.1") or "")


def test_anticipada_advierte_nombres_con_fc() -> None:
    anticipada = AnticipadaStrategy()

    assert anticipada.advertencia_nombre("Pospago Conectados 5.1") is None
    assert "propio de Corriente" in (anticipada.advertencia_nombre("Plan 5.1 FC") or "")

@pytest.mark.parametrize(
    ("tipo", "sufijo"), [(BillingType.CORRIENTE, "Corriente"), (BillingType.ANTICIPADA, "")]
)
def test_sufijo_de_las_claves_de_propiedades(tipo: BillingType, sufijo: str) -> None:
    assert estrategia_para(tipo).sufijo_propiedades == sufijo