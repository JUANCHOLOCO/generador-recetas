from recetas.modules.creacion_planes_pospago.domain.tipos import TipoPaquete
from recetas.modules.creacion_planes_pospago.generators.promotions import filas_poid
from tests.factories import crear_parametrizacion, crear_plan

IDENTIFY = {TipoPaquete.PLAN: "21", TipoPaquete.SMS: "22", TipoPaquete.DATA: "23"}


def test_tres_filas_por_plan_con_poid_real_e_identify() -> None:
    filas = filas_poid(crear_plan(), crear_parametrizacion(identify=IDENTIFY))

    assert [(f.nombre, f.poid, f.identify) for f in filas] == [
        ("Pospago Conectados 5.1 FC", "120617", "21"),
        ("Paquete Conectados SMS 5.1 FC", "990001008", "22"),
        ("Paquete Conectados Datos 5.1 FC", "990000885", "23"),
    ]
    assert filas[1].descripcion == "Descuento Pospago Conectados 5.1 FC sms"
