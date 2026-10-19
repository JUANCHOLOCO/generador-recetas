import pytest
from PySide6.QtWidgets import QLabel
from pytestqt.qtbot import QtBot

from recetas import __version__
from recetas.core.plugins import ModuleRegistry
from recetas.ui.main_window import APP_NAME, MainWindow
from tests.fakes import FakeModule

pytestmark = pytest.mark.ui


def _ventana(qtbot: QtBot, *modulos: FakeModule) -> MainWindow:
    registry = ModuleRegistry()
    for modulo in modulos:
        registry.register(modulo)
    window = MainWindow(registry)
    qtbot.addWidget(window)
    return window


def test_titulo_muestra_nombre_y_version(qtbot: QtBot) -> None:
    window = _ventana(qtbot)

    assert window.windowTitle() == f"{APP_NAME} {__version__}"


def test_sin_seleccion_muestra_bienvenida(qtbot: QtBot) -> None:
    window = _ventana(qtbot, FakeModule("alfa", "Alfa"))

    assert isinstance(window.current_widget, QLabel)
    assert "Seleccione un módulo" in window.current_widget.text()


def test_menu_lista_los_modulos_en_orden(qtbot: QtBot) -> None:
    window = _ventana(qtbot, FakeModule("b", "Beta", order=2), FakeModule("a", "Alfa", order=1))

    assert window.module_names() == ["Alfa", "Beta"]


def test_seleccionar_en_el_menu_muestra_el_widget_del_modulo(qtbot: QtBot) -> None:
    window = _ventana(qtbot, FakeModule("alfa", "Alfa"))

    window.menu.setCurrentRow(0)

    assert isinstance(window.current_widget, QLabel)
    assert window.current_widget.text() == "Widget de Alfa"


def test_el_widget_de_un_modulo_se_crea_una_sola_vez(qtbot: QtBot) -> None:
    modulo = FakeModule("alfa", "Alfa")
    window = _ventana(qtbot, modulo)

    window.show_module("alfa")
    window.show_module("alfa")

    assert modulo.widgets_creados == 1