"""Errores de negocio del módulo Pospago."""

from recetas.core.domain.errors import RecetasError


class ParametrizacionIncompletaError(RecetasError):
    """Falta un dato de parametrización necesario para generar la receta."""