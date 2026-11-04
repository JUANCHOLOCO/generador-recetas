from datetime import date

from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.alza_tarifas.generators.paquetes import AlzaPaquetesGenerator
from tests.factories import crear_solicitud_paquetes

RENDERER = JinjaRenderer("recetas.modules.alza_tarifas", "recetas.core")
BASE = "AlzaPaquetes/Script/ACTIVADOR"
APLICA = f"{BASE}/SQL/1_UPDATE_TPFB-1726_PAQUETES_SCRIPT.SQL"
ROLLBACK = f"{BASE}/ROLLBACK/1_ROLLBACK_UPDATE_TPFB-1726_PAQUETES_SCRIPT.SQL"


def generar() -> RecipeBundle:
    bundle = RecipeBundle("TPFB-1726_Prod")
    AlzaPaquetesGenerator(RENDERER).generar(
        crear_solicitud_paquetes(), date(2026, 11, 4), "0.1.0", bundle
    )
    return bundle


def test_genera_los_4_archivos_en_la_carpeta_de_paquetes() -> None:
    assert [str(f.path) for f in generar().files] == [
        ROLLBACK,
        APLICA,
        f"{BASE}/aplica-cambio.sql",
        f"{BASE}/rollback-cambio.sql",
    ]


def test_services_lleva_el_precio_con_iva_y_atp_los_dos_precios() -> None:
    bundle = generar()
    aplica = bundle.get(APLICA).content
    rollback = bundle.get(ROLLBACK).content

    assert "-- Paquete: Paquete Datos Corporativo 4.0 Plus" in aplica
    assert (
        "UPDATE ACTIVATOR.SERVICES SET ITEM_PRICE=13990 WHERE ID='28708' AND PART_NUM='SVALL2322';"
    ) in aplica
    assert (
        "UPDATE ACTIVATOR.ATP_CORP_PRECIOS_SERVICE SET ITEM_PRICE=11756, ITEM_PRICE_IVA=13990 "
        "WHERE PART_NUM='SVALL2322';"
    ) in aplica
    assert "SET ITEM_PRICE=10605.04, ITEM_PRICE_IVA=12620 WHERE PART_NUM='SVALL2322';" in rollback


def test_el_lanzador_llama_al_script_de_paquetes() -> None:
    lanzador = generar().get(f"{BASE}/rollback-cambio.sql").content

    assert "ALTER SESSION SET CURRENT_SCHEMA=ACTIVATOR;" in lanzador
    assert "@ROLLBACK/1_ROLLBACK_UPDATE_TPFB-1726_PAQUETES_SCRIPT.SQL" in lanzador
