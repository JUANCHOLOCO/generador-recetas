"""Dobles de prueba reutilizables."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date

from PySide6.QtWidgets import QLabel, QWidget

from recetas.core.domain.billing import BillingType
from recetas.core.plugins import Module, ModuleInfo
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion


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


@dataclass(frozen=True)
class RelojFijo:
    fecha: date

    def hoy(self) -> date:
        return self.fecha


class ParametrizacionEnMemoria:
    """Cumple ParametrizacionRepository sin base de datos."""

    def __init__(self, por_tipo: Mapping[BillingType, Parametrizacion]) -> None:
        self._por_tipo = por_tipo

    def cargar(self, tipo: BillingType) -> Parametrizacion:
        return self._por_tipo[tipo]
