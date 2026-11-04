"""Golden del alza de paquetes TPFB-1726, con la corrección declarada de SERVICES."""

import json
import re

import pytest

from recetas.modules.alza_tarifas.application.generar_alza import (
    AlzaGenerada,
    GenerarAlzaPaquetes,
)
from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPaquetes
from tests.fakes import RelojFijo
from tests.golden.alza_tarifas.comun import CASO, RENDERER, original, sentencias
from tests.golden.conftest import FECHA, VERSION

pytestmark = pytest.mark.golden

BASE = "AlzaPaquetes/Script/ACTIVADOR"
_PRECIO_SERVICES = re.compile(r"^(UPDATE ACTIVATOR\.SERVICES SET ITEM_PRICE=)[\d.]+")
_PRECIO_CON_IVA = re.compile(r"ITEM_PRICE_IVA=([\d.]+)")


def con_services_corregido(originales: list[str]) -> list[str]:
    """Corrección declarada (2026-10-29): SERVICES.ITEM_PRICE lleva el precio CON IVA.

    Cada paquete son 2 sentencias: SERVICES y luego ATP_CORP_PRECIOS_SERVICE. El aplica
    real pone en SERVICES el precio sin IVA; se reemplaza por el ITEM_PRICE_IVA de ATP.
    """
    corregidas = list(originales)
    for i in range(0, len(corregidas), 2):
        con_iva = _PRECIO_CON_IVA.search(corregidas[i + 1])
        assert con_iva is not None
        corregidas[i] = _PRECIO_SERVICES.sub(rf"\g<1>{con_iva.group(1)}", corregidas[i])
    return corregidas


@pytest.fixture(scope="module")
def alza() -> AlzaGenerada:
    entrada = json.loads((CASO / "entrada_paquetes.json").read_text(encoding="utf-8"))
    solicitud = SolicitudAlzaPaquetes.model_validate(entrada)
    return GenerarAlzaPaquetes(RENDERER, RelojFijo(FECHA), VERSION).ejecutar(solicitud)


def test_aplica_igual_al_original_con_services_corregido(alza: AlzaGenerada) -> None:
    aplica = alza.bundle.get(f"{BASE}/SQL/1_UPDATE_TPFB-1726_PAQUETES_SCRIPT.SQL")
    originales = sentencias(original("paquetes_aplica.sql"))
    corregidas = con_services_corregido(originales)

    generadas = sentencias(aplica.content)

    assert len(generadas) == 566  # 283 paquetes x 2 sentencias
    assert sum(a != b for a, b in zip(originales, corregidas, strict=True)) == 265
    assert generadas == corregidas


def test_rollback_tiene_las_mismas_sentencias_que_el_original(alza: AlzaGenerada) -> None:
    rollback = alza.bundle.get(f"{BASE}/ROLLBACK/1_ROLLBACK_UPDATE_TPFB-1726_PAQUETES_SCRIPT.SQL")

    assert sentencias(rollback.content) == sentencias(original("paquetes_rollback.sql"))


def test_avisa_los_combo_mintic_en_cero(alza: AlzaGenerada) -> None:
    assert [a.fila for a in alza.advertencias] == [281, 282, 283]
