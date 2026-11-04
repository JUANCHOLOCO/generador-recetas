from recetas.modules.alza_tarifas.domain.advertencias import Advertencia, advertencias_planes
from tests.factories import crear_solicitud_alza, datos_plan_alza


def test_alza_normal_no_avisa() -> None:
    assert advertencias_planes(crear_solicitud_alza()) == ()


def test_precio_nuevo_menor_que_el_actual_avisa() -> None:
    solicitud = crear_solicitud_alza(datos_plan_alza(precio_nuevo="60000"))

    assert advertencias_planes(solicitud) == (
        Advertencia("PLCON0335: el precio nuevo (60000) es menor que el actual (61950).", 1),
    )


def test_precio_nuevo_en_cero_avisa() -> None:
    solicitud = crear_solicitud_alza(datos_plan_alza(precio_nuevo="0"))

    assert advertencias_planes(solicitud) == (Advertencia("PLCON0335: el precio nuevo es 0.", 1),)
