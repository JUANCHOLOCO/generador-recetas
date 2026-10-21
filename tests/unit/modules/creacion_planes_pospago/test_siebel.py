from recetas.modules.creacion_planes_pospago.generators.siebel import (
    cancela_cp_planes,
    plan_siebel,
)
from tests.factories import crear_plan


def test_lista_de_valores_une_pool_svalls_y_part_num() -> None:
    plan = plan_siebel(crear_plan(), ("LNALL0167", "SMALL0103", "PQCON0127"))

    assert plan.lista_de_valores == "LNALL0167|SMALL0103|PQCON0127|SVALL2632|SVALL2640|PLCON0454|"


def test_poid_del_plan_es_el_tarif_group_en_product_y_deal() -> None:
    producto = plan_siebel(crear_plan(), ()).plan

    assert producto.product() == "0.0.0.1 /product 120617 1"
    assert producto.deal() == "0.0.0.1 /deal 120617 0"
    assert producto.product("999999999") == "0.0.0.1 /product 999999999 1"


def test_ordenes_de_los_productos_como_en_los_ejemplos() -> None:
    plan = plan_siebel(crear_plan(), ())

    assert [p.tipo for p in plan.orden_alta] == ["TELEFONIA_POS", "DATA", "SMS"]
    assert [p.tipo for p in plan.orden_atributos] == ["TELEFONIA_POS", "SMS", "DATA"]


def test_cancela_cp_planes_entre_corchetes() -> None:
    assert cancela_cp_planes(["7401", "7751"]) == "[7401][7751]"