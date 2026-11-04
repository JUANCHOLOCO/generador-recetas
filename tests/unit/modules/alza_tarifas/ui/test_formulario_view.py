import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from recetas.modules.alza_tarifas.ui.formulario_presenter import ErrorCampo
from recetas.modules.alza_tarifas.ui.formulario_view import FormularioAlzaView
from recetas.modules.alza_tarifas.ui.tipos_formulario import PAQUETES, PLANES

pytestmark = pytest.mark.ui


def test_lee_lo_escrito_y_marca_errores_en_la_tabla(qtbot: QtBot) -> None:
    vista = FormularioAlzaView(PLANES, "jbotero", "C:/recetas")
    qtbot.addWidget(vista)

    datos = vista.datos()
    vista.mostrar_errores([ErrorCampo("Fila 1 › Part_num: formato", fila=0, columna=1)])

    assert (datos.requerimiento, datos.autor, datos.ambiente, datos.carpeta) == (
        "",
        "jbotero",
        "PROD",
        "C:/recetas",
    )
    assert datos.filas == [[""] * len(PLANES.columnas)]
    celda = vista._modelo.index(0, 1)
    assert vista._modelo.data(celda, Qt.ItemDataRole.ToolTipRole) == "Fila 1 › Part_num: formato"


def test_los_encabezados_explican_el_formato(qtbot: QtBot) -> None:
    vista = FormularioAlzaView(PLANES, "jbotero", "C:/recetas")
    qtbot.addWidget(vista)

    ayuda = vista._modelo.headerData(1, Qt.Orientation.Horizontal, Qt.ItemDataRole.ToolTipRole)

    assert ayuda == "PLCON#### (ej. PLCON0335)"


def test_limpiar_vacia_requerimiento_y_planes_pero_conserva_el_autor(qtbot: QtBot) -> None:
    vista = FormularioAlzaView(PLANES, "jbotero", "C:/recetas")
    qtbot.addWidget(vista)
    vista._requerimiento.setText("TPFB-1726")
    vista.cargar_filas([["x"] * len(PLANES.columnas)] * 2)

    vista.limpiar()

    datos = vista.datos()
    assert (datos.requerimiento, datos.autor) == ("", "jbotero")
    assert datos.filas == [[""] * len(PLANES.columnas)]


def test_la_pestana_de_paquetes_muestra_sus_columnas(qtbot: QtBot) -> None:
    vista = FormularioAlzaView(PAQUETES, "jbotero", "C:/recetas")
    qtbot.addWidget(vista)
    horizontal = Qt.Orientation.Horizontal

    titulos = [
        vista._modelo.headerData(i, horizontal, Qt.ItemDataRole.DisplayRole)
        for i in range(len(PAQUETES.columnas))
    ]

    assert titulos == [c.titulo for c in PAQUETES.columnas]
    ayuda = vista._modelo.headerData(1, horizontal, Qt.ItemDataRole.ToolTipRole)
    assert ayuda == "SVALL#### (ej. SVALL2322)"
