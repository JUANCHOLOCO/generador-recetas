"""Registro del módulo Creación de planes Pospago."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget

from recetas.core.plugins import AppContext, Module, ModuleInfo
from recetas.modules.creacion_planes_pospago.infrastructure.seeds import (
    cargar_parametrizacion_inicial,
)

INFO = ModuleInfo(
    id="creacion_planes_pospago",
    name="Creación de planes Pospago",
    description="Genera los instaladores SQL para nuevos planes Pospago (Corriente o Anticipada).",
    order=10,
)

class CreacionPlanesPospagoModule(Module):
    def __init__(self, context: AppContext) -> None:
        self._context = context

    @property
    def info(self) -> ModuleInfo:
        return INFO

    def initialize(self) -> None:
        cargar_parametrizacion_inicial(self._context.session_factory)

    def create_widget(self, parent: QWidget | None = None) -> QWidget:
        # Provisional: en la Fase 7 será el formulario completo.
        label = QLabel("Creación de planes Pospago: en construcción.", parent)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label