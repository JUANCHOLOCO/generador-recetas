"""API pública del sistema de módulos."""

from recetas.core.plugins.module import Module, ModuleInfo
from recetas.core.plugins.registry import ModuleRegistry

__all__ = ["Module", "ModuleInfo", "ModuleRegistry"]
