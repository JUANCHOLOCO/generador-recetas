"""Ventana principal: menú lateral con los módulos registrados y área de trabajo."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from recetas import __version__
from recetas.core.plugins import ModuleRegistry

APP_NAME = "Generador de Recetas"


class MainWindow(QMainWindow):
    def __init__(self, registry: ModuleRegistry) -> None:
        super().__init__()
        self._registry = registry
        self._widgets: dict[str, QWidget] = {}

        self.setWindowTitle(f"{APP_NAME} {__version__}")
        self.resize(1200, 750)

        self._menu = QListWidget()
        self._menu.setFixedWidth(240)
        for module in registry.modules():
            item = QListWidgetItem(module.info.name)
            item.setData(Qt.ItemDataRole.UserRole, module.info.id)
            item.setToolTip(module.info.description)
            self._menu.addItem(item)

        self._bienvenida = QLabel("Seleccione un módulo para comenzar.")
        self._bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._stack = QStackedWidget()
        self._stack.addWidget(self._bienvenida)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.addWidget(self._menu)
        layout.addWidget(self._stack, stretch=1)
        self.setCentralWidget(central)

        self._menu.currentItemChanged.connect(self._on_item_changed)

    @property
    def menu(self) -> QListWidget:
        return self._menu

    @property
    def current_widget(self) -> QWidget:
        widget = self._stack.currentWidget()
        if widget is None:
            # No debería ocurrir: la bienvenida se agrega en __init__ y nunca se quita.
            raise RuntimeError("La pila de pantallas está vacía.")
        return widget

    def module_names(self) -> list[str]:
        return [self._menu.item(i).text() for i in range(self._menu.count())]

    def show_module(self, module_id: str) -> None:
        widget = self._widgets.get(module_id)
        if widget is None:
            widget = self._registry.get(module_id).create_widget()
            self._widgets[module_id] = widget
            self._stack.addWidget(widget)
        self._stack.setCurrentWidget(widget)

    def _on_item_changed(
        self, current: QListWidgetItem | None, _previous: QListWidgetItem | None
    ) -> None:
        if current is None:
            self._stack.setCurrentWidget(self._bienvenida)
            return
        module_id: str = current.data(Qt.ItemDataRole.UserRole)
        self.show_module(module_id)
