import pytest

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.advertencias import (
    Advertencia,
    calcular_advertencias,
)
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import IdCambioPlan
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan
from tests.factories import crear_parametrizacion, crear_solicitud, datos_plan

NINTENDO_FC = (IdCambioPlan("7401", ListaCambioPlan.NINTENDO),)


def test_solicitud_correcta_no_genera_advertencias() -> None:
    parametrizacion = crear_parametrizacion(ids_cambio_plan=NINTENDO_FC)

    assert calcular_advertencias(crear_solicitud(), parametrizacion) == ()


def test_advierte_id_ya_registrado_indicando_la_fila() -> None:
    parametrizacion = crear_parametrizacion(
        ids_cambio_plan=(*NINTENDO_FC, IdCambioPlan("7751", ListaCambioPlan.NINTENDO))
    )

    advertencias = calcular_advertencias(crear_solicitud(), parametrizacion)

    assert advertencias == (
        Advertencia("El Id_Plan 7751 ya está registrado en la parametrización.", 1),
    )


def test_advierte_si_no_hay_planes_nintendo_del_tipo() -> None:
    advertencias = calcular_advertencias(crear_solicitud(), crear_parametrizacion())

    assert len(advertencias) == 1
    assert advertencias[0].fila is None
    assert "No hay planes Nintendo" in advertencias[0].mensaje


def test_corriente_advierte_nombre_de_plan_sin_fc() -> None:
    solicitud = crear_solicitud(planes=[datos_plan(nombre="Pospago Conectados 5.1")])
    parametrizacion = crear_parametrizacion(ids_cambio_plan=NINTENDO_FC)

    [advertencia] = calcular_advertencias(solicitud, parametrizacion)

    assert advertencia.fila == 1
    assert "Pospago Conectados 5.1" in advertencia.mensaje


def test_anticipada_advierte_cada_nombre_con_fc() -> None:
    solicitud = crear_solicitud(tipo="ANTICIPADA")
    parametrizacion = crear_parametrizacion(
        tipo=BillingType.ANTICIPADA,
        ids_cambio_plan=(IdCambioPlan("739", ListaCambioPlan.NINTENDO),),
    )

    advertencias = calcular_advertencias(solicitud, parametrizacion)

    assert len(advertencias) == 3  # plan, paquete de datos y paquete SMS


def test_parametrizacion_de_otro_tipo_es_un_error_de_programacion() -> None:
    parametrizacion = crear_parametrizacion(tipo=BillingType.ANTICIPADA)

    with pytest.raises(ValueError, match="ANTICIPADA"):
        calcular_advertencias(crear_solicitud(), parametrizacion)
