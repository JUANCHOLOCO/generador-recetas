from pathlib import Path

import pytest
from openpyxl import Workbook
from PySide6.QtWidgets import QTabWidget
from pytestqt.qtbot import QtBot

from recetas.config import AppPaths
from recetas.core.infrastructure.files.escritor import EscritorDeRecetas
from recetas.core.infrastructure.files.excel import LectorExcel
from recetas.main import build_context
from recetas.modules.alza_tarifas.module import AlzaTarifasModule
from recetas.modules.alza_tarifas.ui.formulario_presenter import FORMATO_EXCEL
from recetas.modules.alza_tarifas.ui.formulario_view import FormularioAlzaView
from tests.factories import crear_solicitud_alza

pytestmark = pytest.mark.integration

APLICA = "AlzaPlanesPospago/Script/ACTIVADOR/SQL/1_UPDATE_TPFB-1726_PLANES_POSPAGO_SCRIPT.SQL"


def test_el_modulo_genera_y_escribe_el_alza_con_dependencias_reales(tmp_path: Path) -> None:
    modulo = AlzaTarifasModule(build_context(AppPaths(base=tmp_path)))

    alza = modulo.generar_alza().ejecutar(crear_solicitud_alza())
    raiz = EscritorDeRecetas().escribir(alza.bundle, tmp_path)

    contenido = (raiz / APLICA).read_bytes()
    assert b"ITEM_PRICE=68083, VENDOR_VALUE=68083" in contenido
    assert contenido.count(b"\n") == contenido.count(b"\r\n")  # todo CRLF


def test_el_modulo_muestra_la_pestana_de_planes_pospago(tmp_path: Path, qtbot: QtBot) -> None:
    widget = AlzaTarifasModule(build_context(AppPaths(base=tmp_path))).create_widget()
    qtbot.addWidget(widget)

    assert isinstance(widget, QTabWidget)
    assert widget.tabText(0) == "Planes pospago"
    assert isinstance(widget.widget(0), FormularioAlzaView)


def test_importa_un_excel_con_los_titulos_de_la_tabla(tmp_path: Path) -> None:
    libro = Workbook()
    hoja = libro.active
    hoja.append(list(FORMATO_EXCEL.encabezados))
    hoja.append([1208, "PLCON0335", "Pospago 5.1 Empresarial", 68083, 56320, 61950, 51246.3])
    ruta = tmp_path / "alza.xlsx"
    libro.save(ruta)

    assert LectorExcel().leer(ruta, FORMATO_EXCEL) == [
        ["1208", "PLCON0335", "Pospago 5.1 Empresarial", "68083", "56320", "61950", "51246.3"]
    ]
