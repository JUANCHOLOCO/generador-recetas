"""Importa los modelos ORM de todos los módulos para registrarlos en Base.metadata.

Alembic y los tests importan este archivo. Agregar un módulo con tablas = añadir su import aquí.
"""

from recetas.modules.creacion_planes_pospago.infrastructure import models as pospago_models

__all__ = ["pospago_models"]
