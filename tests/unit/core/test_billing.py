import pytest

from recetas.core.domain.billing import BillingType
from recetas.core.domain.billing import BillingScope


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

@pytest.mark.parametrize(
    ("scope", "billing", "esperado"),
    [
        (BillingScope.AMBAS, BillingType.CORRIENTE, True),
        (BillingScope.AMBAS, BillingType.ANTICIPADA, True),
        (BillingScope.CORRIENTE, BillingType.CORRIENTE, True),
        (BillingScope.CORRIENTE, BillingType.ANTICIPADA, False),
        (BillingScope.ANTICIPADA, BillingType.ANTICIPADA, True),
        (BillingScope.ANTICIPADA, BillingType.CORRIENTE, False),
    ],
)
def test_scope_aplica_a_facturacion(
    scope: BillingScope, billing: BillingType, esperado: bool
) -> None:
    assert scope.applies_to(billing) is esperado


def test_for_billing_incluye_el_tipo_y_ambas() -> None:
    assert BillingScope.for_billing(BillingType.CORRIENTE) == (
        BillingScope.CORRIENTE,
        BillingScope.AMBAS,
    )