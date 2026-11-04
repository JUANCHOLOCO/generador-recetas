"""Golden del alza de planes TPFB-1726: mismas sentencias que la receta real."""

import json
import re
from decimal import Decimal
from pathlib import Path

import pytest

from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.alza_tarifas.application.generar_alza import AlzaGenerada, GenerarAlzaPlanes
from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPlanes
from tests.fakes import RelojFijo
from tests.golden.conftest import FECHA, VERSION

pytestmark = pytest.mark.golden

CASO = Path(__file__).parent / "TPFB-1726"
RENDERER = JinjaRenderer("recetas.modules.alza_tarifas", "recetas.core")
BASE = "AlzaPlanesPospago/Script/ACTIVADOR"
_NUMERO_ENTRE_COMILLAS = re.compile(r"'(\d+(?:,\d+)?)'")


def sentencias(texto: str) -> list[str]:
    """Los UPDATE del script, comparables: espacios unificados y números sin comillas con punto."""
    resultado = []
    for linea in texto.splitlines():
        linea = " ".join(linea.split())
        if linea.upper().startswith("UPDATE "):
            resultado.append(
                _NUMERO_ENTRE_COMILLAS.sub(
                    lambda m: str(Decimal(m.group(1).replace(",", "."))), linea
                )
            )
    return resultado


def original(nombre: str) -> str:
    return (CASO / "original" / nombre).read_text(encoding="cp1252")


@pytest.fixture(scope="module")
def alza() -> AlzaGenerada:
    entrada = json.loads((CASO / "entrada_planes_pospago.json").read_text(encoding="utf-8"))
    solicitud = SolicitudAlzaPlanes.model_validate(entrada)
    return GenerarAlzaPlanes(RENDERER, RelojFijo(FECHA), VERSION).ejecutar(solicitud)


def test_aplica_tiene_las_mismas_sentencias_que_el_original(alza: AlzaGenerada) -> None:
    aplica = alza.bundle.get(f"{BASE}/SQL/1_UPDATE_TPFB-1726_PLANES_POSPAGO_SCRIPT.SQL")

    generadas = sentencias(aplica.content)

    assert len(generadas) == 27
    assert generadas == sentencias(original("planes_aplica.sql"))


def test_rollback_tiene_las_mismas_sentencias_que_el_original(alza: AlzaGenerada) -> None:
    rollback = alza.bundle.get(
        f"{BASE}/ROLLBACK/1_ROLLBACK_UPDATE_TPFB-1726_PLANES_POSPAGO_SCRIPT.SQL"
    )

    assert sentencias(rollback.content) == sentencias(original("planes_rollback.sql"))


def test_avisa_el_plan_cuyo_precio_baja(alza: AlzaGenerada) -> None:
    # Plan Tigo Empresarial 6.7: pasa de 69320 a 68400
    assert [a.fila for a in alza.advertencias] == [26]
