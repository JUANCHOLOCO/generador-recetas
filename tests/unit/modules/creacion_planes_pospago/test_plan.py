from typing import Any

import pytest
from pydantic import ValidationError

from recetas.core.domain.billing import BillingType
from tests.factories import crear_plan, crear_solicitud, datos_plan


def _plan_52(**cambios: Any) -> dict[str, Any]:
    return datos_plan(
        id_plan="7761",
        part_num="PLCON0455",
        nombre="Pospago Conectados 5.2 FC",
        datos={"nombre": "Paquete Conectados Datos 5.2 FC", "svall": "SVALL2633", "poid": "1"},
        sms={"nombre": "Paquete Conectados SMS 5.2 FC", "svall": "SVALL2641", "poid": "2"},
        **cambios,
    )


# ---------- PlanNuevo ----------


def test_plan_de_tpfb_2753_es_valido_y_calcula_derivados() -> None:
    plan = crear_plan()

    assert plan.pcrf_code == "MONTH/Conectados_51_FC"
    assert plan.poid_plan == "120617"
    assert plan.datos.svall == "SVALL2632"


def test_valores_llegan_como_texto_desde_el_formulario() -> None:
    plan = crear_plan(valor_con_iva="19900", valor_sin_iva="16723")

    assert plan.valor_con_iva == 19900


def test_valor_sin_iva_no_puede_superar_al_con_iva() -> None:
    with pytest.raises(ValidationError, match="sin IVA debe ser menor"):
        crear_plan(valor_sin_iva=19900)


def test_reporta_todos_los_errores_con_su_ubicacion() -> None:
    datos = datos_plan(part_num="X", sms={"nombre": "", "svall": "Y", "poid": "1"})

    with pytest.raises(ValidationError) as error:
        crear_plan(**datos)

    ubicaciones = {e["loc"] for e in error.value.errors()}
    assert ubicaciones == {("part_num",), ("sms", "nombre"), ("sms", "svall")}


def test_plan_es_inmutable() -> None:
    plan = crear_plan()

    with pytest.raises(ValidationError):
        plan.nombre = "Otro"  # type: ignore[misc]


def test_campo_desconocido_es_rechazado() -> None:
    with pytest.raises(ValidationError, match="color"):
        crear_plan(color="rojo")


# ---------- SolicitudReceta ----------


def test_solicitud_convierte_el_tipo_de_facturacion() -> None:
    assert crear_solicitud().tipo is BillingType.CORRIENTE


def test_solicitud_sin_planes_falla() -> None:
    with pytest.raises(ValidationError, match="al menos un plan"):
        crear_solicitud(planes=[])


def test_dos_planes_distintos_son_validos() -> None:
    solicitud = crear_solicitud(planes=[datos_plan(), _plan_52()])

    assert [p.id_plan for p in solicitud.planes] == ["7751", "7761"]


def test_detecta_ids_part_nums_y_svalls_repetidos() -> None:
    with pytest.raises(ValidationError) as error:
        crear_solicitud(planes=[datos_plan(), datos_plan()])

    mensaje = str(error.value)
    assert "Id_Plan repetido: 7751" in mensaje
    assert "Part_num repetido: PLCON0454" in mensaje
    assert "Svall repetido: SVALL2632" in mensaje


def test_svall_de_datos_igual_al_de_sms_es_repetido() -> None:
    plan = datos_plan(sms={"nombre": "SMS", "svall": "SVALL2632", "poid": "1"})

    with pytest.raises(ValidationError, match="Svall repetido: SVALL2632"):
        crear_solicitud(planes=[plan])


def test_autor_es_obligatorio() -> None:
    with pytest.raises(ValidationError) as error:
        crear_solicitud(autor="  ")

    assert {e["loc"] for e in error.value.errors()} == {("autor",)}
