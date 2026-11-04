"""Advertencias del alza: no bloquean, el usuario decide si genera de todos modos."""

from dataclasses import dataclass

from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPlanes


@dataclass(frozen=True, slots=True)
class Advertencia:
    mensaje: str
    fila: int | None = None  # número del plan (desde 1)


def advertencias_planes(solicitud: SolicitudAlzaPlanes) -> tuple[Advertencia, ...]:
    advertencias: list[Advertencia] = []
    for numero, plan in enumerate(solicitud.planes, start=1):
        if plan.precio_nuevo == 0:
            advertencias.append(Advertencia(f"{plan.part_num}: el precio nuevo es 0.", numero))
        elif plan.precio_nuevo < plan.precio_actual:
            advertencias.append(
                Advertencia(
                    f"{plan.part_num}: el precio nuevo ({plan.precio_nuevo}) es menor que el "
                    f"actual ({plan.precio_actual}).",
                    numero,
                )
            )
    return tuple(advertencias)
