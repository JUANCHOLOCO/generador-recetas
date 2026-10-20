"""Puertos: lo que el módulo necesita del exterior, expresado como interfaces."""

from typing import Protocol

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion


class ParametrizacionRepository(Protocol):
    def cargar(self, tipo: BillingType) -> Parametrizacion:
        """Parametrización activa que aplica al tipo de facturación indicado."""
        ...
