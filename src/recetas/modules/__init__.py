"""Módulos instalados. Agregar un módulo nuevo = añadirlo a esta lista."""

from recetas.core.plugins import AppContext, Module
from recetas.modules.creacion_planes_pospago.module import CreacionPlanesPospagoModule

def installed_modules(context: AppContext) -> list[Module]:
    return [
        CreacionPlanesPospagoModule(context),
    ]