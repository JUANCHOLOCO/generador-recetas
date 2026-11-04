import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from recetas.modules.creacion_planes_pospago.ui.formulario_presenter import COLUMNAS, ErrorCampo
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


def test_cargar_planes_reemplaza_las_filas(qtbot: QtBot) -> None:
    vista = FormularioView("jbotero", "C:/recetas")
    qtbot.addWidget(vista)
    filas = [[str(i)] * len(COLUMNAS) for i in range(2)]

    vista.cargar_planes(filas)

    assert vista.datos().filas == filas


def test_limpiar_vacia_requerimiento_tipo_y_planes_pero_conserva_el_autor(qtbot: QtBot) -> None:
    vista = FormularioView("jbotero", "C:/recetas")
    qtbot.addWidget(vista)
    vista._requerimiento.setText("TPFB-1")
    vista._corriente.setChecked(True)
    vista.cargar_planes([["x"] * len(COLUMNAS)] * 2)

    vista.limpiar()

    datos = vista.datos()
    assert (datos.requerimiento, datos.tipo, datos.autor) == ("", "", "jbotero")
    assert datos.filas == [[""] * len(COLUMNAS)]


def test_los_encabezados_explican_el_formato(qtbot: QtBot) -> None:
    vista = FormularioView("jbotero", "C:/recetas")
    qtbot.addWidget(vista)

    ayuda = vista._modelo.headerData(1, Qt.Orientation.Horizontal, Qt.ItemDataRole.ToolTipRole)

    assert ayuda == "PLCON#### (ej. PLCON0454)"
    assert all(c.ayuda for c in COLUMNAS)
