import pytest
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from recetas.ui.widgets.atajos import conectar_generar
from recetas.ui.widgets.tabla_editable import TablaEditable, TablaEditableModel

pytestmark = pytest.mark.ui


def test_ctrl_enter_genera_desde_el_formulario(qtbot: QtBot) -> None:
    formulario = QWidget()
    qtbot.addWidget(formulario)
    tabla = TablaEditable(TablaEditableModel(["A"]), formulario)
    llamadas: list[str] = []

    conectar_generar(formulario, tabla, lambda: llamadas.append("generar"))
    atajos = formulario.findChildren(QShortcut)
    atajos[0].activated.emit()

    assert sorted(a.key().toString() for a in atajos) == ["Ctrl+Enter", "Ctrl+Return"]
    assert llamadas == ["generar"]
