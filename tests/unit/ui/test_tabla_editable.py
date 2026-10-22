import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtWidgets import QApplication

from recetas.ui.widgets.tabla_editable import TablaEditableModel

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
