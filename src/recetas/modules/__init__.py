"""Módulos instalados. Agregar un módulo nuevo = añadirlo a esta lista."""

from recetas.core.plugins import Module
from recetas.modules.creacion_planes_pospago.module import CreacionPlanesPospagoModule


def installed_modules() -> list[Module]:
    return [
        CreacionPlanesPospagoModule(),
    ]