"""Advertencias que no bloquean la generación: el usuario decide si continúa."""

from dataclasses import dataclass

from recetas.modules.creacion_planes_pospago.domain.estrategias import estrategia_para
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan


@dataclass(frozen=True, slots=True)
class Advertencia:
    mensaje: str
    fila: int | None = None  # 1 = primera fila del formulario; None = advertencia general


def calcular_advertencias(
    solicitud: SolicitudReceta, parametrizacion: Parametrizacion
) -> tuple[Advertencia, ...]:
    if parametrizacion.tipo is not solicitud.tipo:
        raise ValueError(
            f"La parametrización es de {parametrizacion.tipo} y la solicitud de {solicitud.tipo}."
        )

    estrategia = estrategia_para(solicitud.tipo)
    advertencias: list[Advertencia] = []

    if not parametrizacion.ids_de_lista(ListaCambioPlan.NINTENDO):
        advertencias.append(
            Advertencia(
                f"No hay planes Nintendo configurados para {solicitud.tipo.label}: la matriz "
                "de cambios de plan solo incluirá Prepago y los planes de este formulario."
            )
        )

    registrados = {i.id_plan for i in parametrizacion.ids_cambio_plan}
    for fila, plan in enumerate(solicitud.planes, start=1):
        if plan.id_plan in registrados:
            advertencias.append(
                Advertencia(
                    f"El Id_Plan {plan.id_plan} ya está registrado en la parametrización.", fila
                )
            )
        for nombre in (plan.nombre, plan.datos.nombre, plan.sms.nombre):
            if (mensaje := estrategia.advertencia_nombre(nombre)) is not None:
                advertencias.append(Advertencia(mensaje, fila))

    return tuple(advertencias)