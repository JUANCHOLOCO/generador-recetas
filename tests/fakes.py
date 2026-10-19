"""Dobles de prueba reutilizables."""

from PySide6.QtWidgets import QLabel, QWidget

from recetas.core.plugins import Module, ModuleInfo


class FakeModule(Module):
    def __init__(self, id_: str, name: str, order: int = 100) -> None:
        self._info = ModuleInfo(id=id_, name=name, order=order)
        self.widgets_creados = 0

    @property
    def info(self) -> ModuleInfo:
        return self._info

    def create_widget(self, parent: QWidget | None = None) -> QWidget:
        self.widgets_creados += 1
        return QLabel(f"Widget de {self._info.name}", parent)
