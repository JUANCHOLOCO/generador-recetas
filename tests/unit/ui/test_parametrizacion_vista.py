import pytest
from pytestqt.qtbot import QtBot

from recetas.core.application.mantenimiento import ColumnaEditable, ErrorCelda
from recetas.ui.parametrizacion.vista import ParametrizacionView

pytestmark = pytest.mark.ui


def test_muestra_la_tabla_oculta_filas_y_marca_errores(qtbot: QtBot) -> None:
    vista = ParametrizacionView(["Canales", "Roles"])
    qtbot.addWidget(vista)
    columnas = [
        ColumnaEditable("nombre", "Nombre"),
        ColumnaEditable("activo", "Activo", ("S", "N")),
    ]

    vista.mostrar_tabla(columnas, [["Retail", "S"], ["Pyme", "N"]], [1, 2])
    vista.mostrar_solo({0})
    vista.mostrar_errores([ErrorCelda("Fila 2 › Activo: Use S o N.", 1, "activo")])

    assert vista.filas() == [["Retail", "S"], ["Pyme", "N"]]
    assert vista.claves() == [1, 2]
    assert vista._tabla.isRowHidden(1)
    assert "Use S o N" in vista._errores.text()
