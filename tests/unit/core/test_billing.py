import pytest

from recetas.core.domain.billing import BillingType


def test_se_construye_desde_texto() -> None:
    assert BillingType("CORRIENTE") is BillingType.CORRIENTE
    assert BillingType("ANTICIPADA") is BillingType.ANTICIPADA


def test_texto_desconocido_falla() -> None:
    with pytest.raises(ValueError):
        BillingType("VENCIDA")


def test_es_comparable_con_str() -> None:
    assert BillingType.CORRIENTE == "CORRIENTE"


@pytest.mark.parametrize(
    ("tipo", "esperado"),
    [
        (BillingType.CORRIENTE, "Corriente (FC)"),
        (BillingType.ANTICIPADA, "Anticipada"),
    ],
)
def test_label_para_la_interfaz(tipo: BillingType, esperado: str) -> None:
    assert tipo.label == esperado