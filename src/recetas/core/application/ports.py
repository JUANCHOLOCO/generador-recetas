"""Puertos del núcleo: servicios que cualquier módulo puede necesitar."""

from datetime import date
from typing import Protocol


class Reloj(Protocol):
    def hoy(self) -> date: ...


class UsuarioActual(Protocol):
    def nombre(self) -> str:
        """Nombre del usuario que genera la receta ('' si no se puede determinar)."""
        ...


class TemplateRenderer(Protocol):
    def render(self, plantilla: str, **contexto: object) -> str: ...
