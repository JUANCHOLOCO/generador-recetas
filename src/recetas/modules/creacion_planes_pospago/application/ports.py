"""Puertos: lo que el módulo necesita del exterior, expresado como interfaces."""

from dataclasses import dataclass
from typing import Protocol

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta


class ParametrizacionRepository(Protocol):
    def cargar(self, tipo: BillingType) -> Parametrizacion:
        """Parametrización activa que aplica al tipo de facturación indicado."""
        ...


@dataclass(frozen=True, slots=True)
class PlanesRegistrados:
    cambio_plan: int
    planes_53: int


class RegistroDePlanes(Protocol):
    def registrar(self, solicitud: SolicitudReceta) -> PlanesRegistrados:
        """Agrega los planes de la solicitud a la parametrización de su tipo (idempotente)."""
        ...
