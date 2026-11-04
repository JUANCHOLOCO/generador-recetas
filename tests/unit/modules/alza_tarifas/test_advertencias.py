from recetas.modules.alza_tarifas.domain.advertencias import (
    Advertencia,
    advertencias_paquetes,
    advertencias_planes,
)
from tests.factories import (
    crear_solicitud_alza,
    crear_solicitud_paquetes,
    datos_paquete_alza,
    datos_plan_alza,
)


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


def test_alza_normal_de_paquetes_no_avisa() -> None:
    assert advertencias_paquetes(crear_solicitud_paquetes()) == ()


def test_paquete_en_cero_avisa() -> None:
    solicitud = crear_solicitud_paquetes(datos_paquete_alza(con_iva_nuevo="0", sin_iva_nuevo="0"))

    assert advertencias_paquetes(solicitud) == (
        Advertencia("SVALL2322: el precio con IVA nuevo es 0.", 1),
    )


def test_paquete_con_precio_menor_que_el_actual_avisa() -> None:
    solicitud = crear_solicitud_paquetes(datos_paquete_alza(con_iva_nuevo="12000"))

    assert advertencias_paquetes(solicitud) == (
        Advertencia(
            "SVALL2322: el precio con IVA nuevo (12000) es menor que el actual (12620).", 1
        ),
    )


def test_precio_sin_iva_mayor_que_con_iva_avisa_en_nuevo_y_en_actual() -> None:
    solicitud = crear_solicitud_paquetes(
        datos_paquete_alza(sin_iva_nuevo="14000", sin_iva_actual="13000")
    )

    assert [a.mensaje for a in advertencias_paquetes(solicitud)] == [
        "SVALL2322: el precio sin IVA nuevo (14000) es mayor que el precio con IVA (13990).",
        "SVALL2322: el precio sin IVA actual (13000) es mayor que el precio con IVA (12620).",
    ]
