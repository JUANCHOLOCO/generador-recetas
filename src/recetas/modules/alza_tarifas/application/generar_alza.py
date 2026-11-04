"""Caso de uso: generar la receta del alza de planes pospago."""

import logging
from dataclasses import dataclass

from recetas.core.application.ports import Reloj, TemplateRenderer
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.modules.alza_tarifas.domain.advertencias import Advertencia, advertencias_planes
from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPlanes
from recetas.modules.alza_tarifas.generators.planes import AlzaPlanesGenerator

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class AlzaGenerada:
    bundle: RecipeBundle
    advertencias: tuple[Advertencia, ...]


class GenerarAlzaPlanes:
    def __init__(self, renderer: TemplateRenderer, reloj: Reloj, version: str) -> None:
        self._generador = AlzaPlanesGenerator(renderer)
        self._reloj = reloj
        self._version = version

    def ejecutar(self, solicitud: SolicitudAlzaPlanes) -> AlzaGenerada:
        bundle = RecipeBundle(f"{solicitud.requerimiento}_{solicitud.ambiente.sufijo}")
        self._generador.generar(solicitud, self._reloj.hoy(), self._version, bundle)
        advertencias = advertencias_planes(solicitud)
        logger.info(
            "Alza de planes %s: %d planes, %d advertencias",
            bundle.root,
            len(solicitud.planes),
            len(advertencias),
        )
        return AlzaGenerada(bundle, advertencias)
