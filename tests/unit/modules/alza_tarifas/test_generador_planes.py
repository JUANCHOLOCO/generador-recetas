from datetime import date

from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPlanes
from recetas.modules.alza_tarifas.generators.planes import AlzaPlanesGenerator
from tests.factories import crear_solicitud_alza

RENDERER = JinjaRenderer("recetas.modules.alza_tarifas", "recetas.core")
BASE = "AlzaPlanesPospago/Script/ACTIVADOR"
APLICA = f"{BASE}/SQL/1_UPDATE_TPFB-1726_PLANES_POSPAGO_SCRIPT.SQL"
ROLLBACK = f"{BASE}/ROLLBACK/1_ROLLBACK_UPDATE_TPFB-1726_PLANES_POSPAGO_SCRIPT.SQL"


def generar(solicitud: SolicitudAlzaPlanes) -> RecipeBundle:
    bundle = RecipeBundle("TPFB-1726_Prod")
    AlzaPlanesGenerator(RENDERER).generar(solicitud, date(2026, 11, 3), "0.1.0", bundle)
    return bundle


def test_genera_los_4_archivos_de_activador() -> None:
    bundle = generar(crear_solicitud_alza())

    assert [str(f.path) for f in bundle.files] == [
        ROLLBACK,
        APLICA,
        f"{BASE}/aplica-cambio.sql",
        f"{BASE}/rollback-cambio.sql",
    ]


def test_aplica_con_precios_nuevos_y_rollback_con_actuales() -> None:
    bundle = generar(crear_solicitud_alza())
    aplica = bundle.get(APLICA).content
    rollback = bundle.get(ROLLBACK).content

    assert "-- Plan: Pospago 5.1 Empresarial" in aplica
    assert (
        "UPDATE ACTIVATOR.PLANS SET ITEM_PRICE=68083, VENDOR_VALUE=68083, "
        "ITEM_PRICE_PRORRATE=56320 WHERE ID='1208' AND PART_NUM='PLCON0335';"
    ) in aplica
    assert (
        "UPDATE ACTIVATOR.PLANS SET ITEM_PRICE=61950, VENDOR_VALUE=61950, "
        "ITEM_PRICE_PRORRATE=51246.3 WHERE ID='1208' AND PART_NUM='PLCON0335';"
    ) in rollback
    assert aplica.rstrip().endswith("HORA_FIN FROM DUAL;")


def test_el_lanzador_llama_al_script_en_activator() -> None:
    lanzador = generar(crear_solicitud_alza()).get(f"{BASE}/aplica-cambio.sql").content

    assert "ALTER SESSION SET CURRENT_SCHEMA=ACTIVATOR;" in lanzador
    assert "@SQL/1_UPDATE_TPFB-1726_PLANES_POSPAGO_SCRIPT.SQL" in lanzador
