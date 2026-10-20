"""Contrato que debe cumplir cada módulo de negocio."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget

_ID_VALIDO = re.compile(r"[a-z][a-z0-9_]*")


@dataclass(frozen=True, slots=True)
class ModuleInfo:
    """Metadatos con los que la app muestra y ordena un módulo."""

    id: str
    name: str
    description: str = ""
    order: int = 100

    def __post_init__(self) -> None:
        if not _ID_VALIDO.fullmatch(self.id):
            raise ValueError(
                f"Id de módulo inválido: '{self.id}'. Use snake_case, ej. 'alza_tarifas'."
            )
        if not self.name.strip():
            raise ValueError("El nombre del módulo no puede estar vacío.")


class Module(ABC):
    """Un módulo de negocio: aporta sus metadatos y su pantalla principal."""

    @property
    @abstractmethod
    def info(self) -> ModuleInfo:
        """Metadatos del módulo."""

    @abstractmethod
    def create_widget(self, parent: QWidget | None = None) -> QWidget:
        """Construye la pantalla principal del módulo."""

    def initialize(self) -> None:  # noqa: B027 (hook opcional: vacío a propósito)
        """Prepara el módulo al iniciar la app, por ejemplo cargando sus datos iniciales."""
