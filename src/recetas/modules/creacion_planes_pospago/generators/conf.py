"""Archivo Conf/Pool-RQ-*.txt: un nombre de plan por línea."""

from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.modules.creacion_planes_pospago.generators.base import ContextoGeneracion


class PoolGenerator:
    def generar(self, ctx: ContextoGeneracion, bundle: RecipeBundle) -> None:
        contenido = "".join(f"{plan.nombre}\n" for plan in ctx.solicitud.planes)
        bundle.add(f"{ctx.estrategia.carpeta}/Conf/Pool-RQ-{ctx.rq}.txt", contenido)