"""Caso de uso: generar la receta completa de una solicitud."""

import logging
from dataclasses import dataclass

from recetas.core.application.ports import Reloj, TemplateRenderer
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.modules.creacion_planes_pospago.application.ports import ParametrizacionRepository
from recetas.modules.creacion_planes_pospago.domain.advertencias import (
    Advertencia,
    calcular_advertencias,
)
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta
from recetas.modules.creacion_planes_pospago.generators.activador import ActivadorGenerator
from recetas.modules.creacion_planes_pospago.generators.base import (
    ContextoGeneracion,
    Generador,
)
from recetas.modules.creacion_planes_pospago.domain.propiedades import (
    ArchivoPropiedades,
    calcular_propiedades,
)
from recetas.modules.creacion_planes_pospago.generators.conf import PoolGenerator
from recetas.modules.creacion_planes_pospago.generators.promotions import PromotionsGenerator
from recetas.modules.creacion_planes_pospago.generators.propiedades import PropiedadesGenerator
from recetas.modules.creacion_planes_pospago.generators.siebel import SiebelGenerator

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RecetaGenerada:
    bundle: RecipeBundle
    advertencias: tuple[Advertencia, ...]
    propiedades: tuple[ArchivoPropiedades, ...]


class GenerarReceta:
    def __init__(
        self,
        parametrizacion: ParametrizacionRepository,
        renderer: TemplateRenderer,
        reloj: Reloj,
        version: str,
    ) -> None:
        self._parametrizacion = parametrizacion
        self._reloj = reloj
        self._version = version
        self._generadores: tuple[Generador, ...] = (
            ActivadorGenerator(renderer),
            SiebelGenerator(renderer),
            PromotionsGenerator(renderer),
            PoolGenerator(),
            PropiedadesGenerator(),
        )

    def ejecutar(self, solicitud: SolicitudReceta) -> RecetaGenerada:
        parametrizacion = self._parametrizacion.cargar(solicitud.tipo)
        ctx = ContextoGeneracion.crear(solicitud, parametrizacion, self._reloj.hoy(), self._version)
        bundle = RecipeBundle(f"{solicitud.requerimiento}_{solicitud.ambiente.sufijo}")
        for generador in self._generadores:
            generador.generar(ctx, bundle)
        logger.info(
            "Receta %s (%s, %s): %d archivos, %d advertencias",
            bundle.root,
            solicitud.tipo,
            solicitud.ambiente,
            len(bundle),
            len(advertencias := calcular_advertencias(solicitud, parametrizacion)),
        )
        propiedades = calcular_propiedades(
            solicitud.planes, parametrizacion.planes_53, ctx.estrategia
        )
        return RecetaGenerada(bundle, advertencias, propiedades)
