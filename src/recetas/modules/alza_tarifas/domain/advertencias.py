"""Advertencias del alza: no bloquean, el usuario decide si genera de todos modos."""

from dataclasses import dataclass
from decimal import Decimal

from recetas.modules.alza_tarifas.domain.solicitud import (
    SolicitudAlzaPaquetes,
    SolicitudAlzaPlanes,
)


@dataclass(frozen=True, slots=True)
class Advertencia:
    mensaje: str
    fila: int | None = None  # número del plan o paquete (desde 1)


def advertencias_planes(solicitud: SolicitudAlzaPlanes) -> tuple[Advertencia, ...]:
    avisos: list[Advertencia] = []
    for fila, plan in enumerate(solicitud.planes, start=1):
        avisos += _precio_nuevo(
            plan.part_num, "precio", plan.precio_nuevo, plan.precio_actual, fila
        )
    return tuple(avisos)


def advertencias_paquetes(solicitud: SolicitudAlzaPaquetes) -> tuple[Advertencia, ...]:
    avisos: list[Advertencia] = []
    for fila, paquete in enumerate(solicitud.paquetes, start=1):
        avisos += _precio_nuevo(
            paquete.part_num, "precio con IVA", paquete.con_iva_nuevo, paquete.con_iva_actual, fila
        )
        precios = (
            ("nuevo", paquete.con_iva_nuevo, paquete.sin_iva_nuevo),
            ("actual", paquete.con_iva_actual, paquete.sin_iva_actual),
        )
        for cuando, con_iva, sin_iva in precios:
            if sin_iva > con_iva:
                avisos.append(
                    Advertencia(
                        f"{paquete.part_num}: el precio sin IVA {cuando} ({sin_iva}) es mayor "
                        f"que el precio con IVA ({con_iva}).",
                        fila,
                    )
                )
    return tuple(avisos)


def _precio_nuevo(
    part_num: str, precio: str, nuevo: Decimal, actual: Decimal, fila: int
) -> list[Advertencia]:
    if nuevo == 0:
        return [Advertencia(f"{part_num}: el {precio} nuevo es 0.", fila)]
    if nuevo < actual:
        return [
            Advertencia(
                f"{part_num}: el {precio} nuevo ({nuevo}) es menor que el actual ({actual}).",
                fila,
            )
        ]
    return []
