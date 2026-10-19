import pytest
from pytestqt.qtbot import QtBot

from recetas import __version__
from recetas.ui.main_window import APP_NAME, MainWindow


@pytest.mark.ui
def test_titulo_muestra_nombre_y_version(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == f"{APP_NAME} {__version__}"
