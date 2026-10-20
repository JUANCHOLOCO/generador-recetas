import pytest

from recetas.modules.creacion_planes_pospago.domain.errors import ParametrizacionIncompletaError
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import (
    CampoEstatico,
    IdCambioPlan,
)
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan, TipoPaquete
from tests.factories import crear_parametrizacion


def test_ids_de_lista_filtra_y_conserva_el_orden() -> None:
    parametrizacion = crear_parametrizacion(
        ids_cambio_plan=(
            IdCambioPlan("1", ListaCambioPlan.PREPAGO),
            IdCambioPlan("7401", ListaCambioPlan.NINTENDO),
            IdCambioPlan("7391", ListaCambioPlan.NINTENDO),
        )
    )

    assert parametrizacion.ids_de_lista(ListaCambioPlan.NINTENDO) == ("7401", "7391")
    assert parametrizacion.ids_de_lista(ListaCambioPlan.CONTROL) == ()


def test_campos_filtra_por_tabla_y_tipo_de_paquete() -> None:
    tipo = CampoEstatico("PLANS", TipoPaquete.PLAN, "TYPE", "'CONTROL'")
    prioridad_data = CampoEstatico("SERVICES", TipoPaquete.DATA, "PRIORITY", "63")
    prioridad_sms = CampoEstatico("SERVICES", TipoPaquete.SMS, "PRIORITY", "63")
    parametrizacion = crear_parametrizacion(campos_estaticos=(tipo, prioridad_data, prioridad_sms))

    assert parametrizacion.campos("SERVICES", TipoPaquete.SMS) == (prioridad_sms,)


def test_identify_de_un_tipo_configurado() -> None:
    parametrizacion = crear_parametrizacion(identify={TipoPaquete.PLAN: "21"})

    assert parametrizacion.identify_de(TipoPaquete.PLAN) == "21"


def test_identify_faltante_lanza_error_de_negocio() -> None:
    with pytest.raises(ParametrizacionIncompletaError, match="SMS"):
        crear_parametrizacion().identify_de(TipoPaquete.SMS)
