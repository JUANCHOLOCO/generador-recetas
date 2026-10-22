"""Puertos del núcleo: servicios que cualquier módulo puede necesitar."""

from datetime import date
from pathlib import Path
from typing import Protocol

from recetas.core.domain.recipe_bundle import RecipeBundle


class Reloj(Protocol):
    def hoy(self) -> date: ...


class UsuarioActual(Protocol):
    def nombre(self) -> str:
        """Nombre del usuario que genera la receta ('' si no se puede determinar)."""
        ...


class TemplateRenderer(Protocol):
    def render(self, plantilla: str, **contexto: object) -> str: ...


class BundleWriter(Protocol):
    def escribir(self, bundle: RecipeBundle, carpeta: Path, *, sobrescribir: bool = False) -> Path:
        """Escribe la receta dentro de `carpeta` y devuelve la ruta de su raíz."""
        ...
