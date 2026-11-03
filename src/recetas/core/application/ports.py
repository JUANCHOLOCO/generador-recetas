"""Puertos del núcleo: servicios que cualquier módulo puede necesitar."""

from datetime import date
from pathlib import Path
from typing import Protocol

from recetas.core.domain.importacion import FormatoHoja
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


class LectorDeHojas(Protocol):
    def leer(self, ruta: Path, formato: FormatoHoja) -> list[list[str]]:
        """Filas de datos de la primera hoja, como texto. Lanza ImportacionError."""
        ...


class Preferencias(Protocol):
    """Valores que la app recuerda entre sesiones. No son críticos: si fallan, se usan los de
    defecto y la app sigue funcionando."""

    def leer(self, clave: str) -> str | None: ...
    def guardar(self, clave: str, valor: str) -> None: ...
