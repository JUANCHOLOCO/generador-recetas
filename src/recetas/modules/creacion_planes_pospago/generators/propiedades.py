"""Archivos Conf/*.properties de la receta."""

from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.modules.creacion_planes_pospago.domain.propiedades import calcular_propiedades
from recetas.modules.creacion_planes_pospago.generators.base import ContextoGeneracion


class PropiedadesGenerator:
    def generar(self, ctx: ContextoGeneracion, bundle: RecipeBundle) -> None:
        archivos = calcular_propiedades(
            ctx.solicitud.planes, ctx.parametrizacion.planes_53, ctx.estrategia
        )
        for archivo in archivos:
            bundle.add(f"{ctx.estrategia.carpeta}/Conf/{archivo.nombre}", archivo.contenido)