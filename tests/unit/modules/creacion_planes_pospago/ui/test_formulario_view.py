import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from recetas.modules.creacion_planes_pospago.ui.formulario_presenter import ErrorCampo
from recetas.modules.creacion_planes_pospago.ui.formulario_view import FormularioView

pytestmark = pytest.mark.ui


def test_lee_lo_escrito_y_marca_errores_en_la_tabla(qtbot: QtBot) -> None:
    vista = FormularioView("jbotero", "C:/recetas")
    qtbot.addWidget(vista)

    datos = vista.datos()
    vista.mostrar_errores([ErrorCampo("Fila 1 › Part_num: formato", fila=0, columna=1)])

    assert (datos.autor, datos.ambiente, datos.tipo, datos.carpeta) == (
        "jbotero",
        "PROD",
        "",
        "C:/recetas",
    )
    celda = vista._modelo.index(0, 1)
    assert vista._modelo.data(celda, Qt.ItemDataRole.ToolTipRole) == "Fila 1 › Part_num: formato"
