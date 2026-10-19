"""Registro del módulo Creación de planes Pospago."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget

from recetas.core.plugins import Module, ModuleInfo

INFO = ModuleInfo(
    id="creacion_planes_pospago",
    name="Creación de planes Pospago",
    description="Genera los instaladores SQL para nuevos planes Pospago (Corriente o Anticipada).",
    order=10,
)


class CreacionPlanesPospagoModule(Module):
    @property
    def info(self) -> ModuleInfo:
        return INFO

    def create_widget(self, parent: QWidget | None = None) -> QWidget:
        # Provisional: en la Fase 7 será el formulario completo.
        label = QLabel("Creación de planes Pospago: en construcción.", parent)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
