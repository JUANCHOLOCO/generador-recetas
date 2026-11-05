import pytest
from PySide6.QtCore import QItemSelectionModel, Qt
from PySide6.QtGui import QBrush
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from recetas.ui.widgets.tabla_editable import TablaEditable, TablaEditableModel

pytestmark = pytest.mark.ui


def _modelo() -> TablaEditableModel:
    return TablaEditableModel(["A", "B", "C"])


def test_pegar_texto_de_excel_agrega_filas(qapp: QApplication) -> None:
    modelo = _modelo()

    pegadas = modelo.pegar("1\t2\t3\r\n4\t5\t6\r\n")

    assert pegadas == 2
    assert modelo.filas() == [["1", "2", "3"], ["4", "5", "6"]]


def test_pegar_desde_una_celda_y_recortar_columnas_sobrantes(qapp: QApplication) -> None:
    modelo = _modelo()
    modelo.agregar_fila()

    modelo.pegar("x\ty\tz\tsobra", fila=0, columna=1)

    assert modelo.filas() == [["", "x", "y"]]


def test_error_se_muestra_y_desaparece_al_editar(qapp: QApplication) -> None:
    modelo = _modelo()
    modelo.agregar_fila()
    celda = modelo.index(0, 1)
    modelo.marcar_errores({(0, 1): "Debe tener el formato SVALL####."})

    assert isinstance(modelo.data(celda, Qt.ItemDataRole.BackgroundRole), QBrush)
    assert "SVALL" in str(modelo.data(celda, Qt.ItemDataRole.ToolTipRole))

    modelo.setData(celda, " SVALL2632 ")

    assert modelo.data(celda, Qt.ItemDataRole.BackgroundRole) is None
    assert modelo.filas()[0][1] == "SVALL2632"


def test_quitar_varias_filas(qapp: QApplication) -> None:
    modelo = _modelo()
    modelo.pegar("1\n2\n3\n4")

    modelo.quitar_filas([0, 2])

    assert [f[0] for f in modelo.filas()] == ["2", "4"]


def test_cargar_cambia_columnas_y_conserva_claves_al_editar(qapp: QApplication) -> None:
    modelo = _modelo()
    modelo.cargar(
        ["X", "Y"], [["1", "a"], ["2", "b"]], claves=[10, 20], ayudas=["", "Valores: a, b"]
    )

    modelo.agregar_fila()
    modelo.quitar_filas([0])

    assert modelo.columnCount() == 2
    assert modelo.filas() == [["2", "b"], ["", ""]]
    assert modelo.claves() == [20, None]
    assert modelo.headerData(1, Qt.Orientation.Horizontal, Qt.ItemDataRole.ToolTipRole) == (
        "Valores: a, b"
    )


def test_supr_vacia_las_celdas_seleccionadas_y_solo_sus_errores(qtbot: QtBot) -> None:
    modelo = _modelo()
    modelo.cargar(["A", "B", "C"], [["1", "2", "3"]])
    modelo.marcar_errores({(0, 0): "mal", (0, 2): "mal"})
    tabla = TablaEditable(modelo)
    qtbot.addWidget(tabla)
    seleccion = tabla.selectionModel()
    for columna in (0, 1):
        seleccion.select(modelo.index(0, columna), QItemSelectionModel.SelectionFlag.Select)

    QTest.keyClick(tabla, Qt.Key.Key_Delete)

    assert modelo.filas() == [["", "", "3"]]
    assert modelo.data(modelo.index(0, 0), Qt.ItemDataRole.ToolTipRole) is None
    assert modelo.data(modelo.index(0, 2), Qt.ItemDataRole.ToolTipRole) == "mal"
