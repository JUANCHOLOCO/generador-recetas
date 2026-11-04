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
from recetas.modules.alza_tarifas.ui.formulario_view import FormularioAlzaView
from recetas.modules.alza_tarifas.ui.tipos_formulario import PAQUETES, PLANES
from tests.factories import crear_solicitud_alza, crear_solicitud_paquetes

pytestmark = pytest.mark.integration

APLICA_PLANES = (
    "AlzaPlanesPospago/Script/ACTIVADOR/SQL/1_UPDATE_TPFB-1726_PLANES_POSPAGO_SCRIPT.SQL"
)
APLICA_PAQUETES = "AlzaPaquetes/Script/ACTIVADOR/SQL/1_UPDATE_TPFB-1726_PAQUETES_SCRIPT.SQL"


def test_planes_y_paquetes_del_mismo_rq_conviven_en_la_receta(tmp_path: Path) -> None:
    modulo = AlzaTarifasModule(build_context(AppPaths(base=tmp_path)))
    escritor = EscritorDeRecetas()

    planes = modulo.generar_alza_planes().ejecutar(crear_solicitud_alza())
    paquetes = modulo.generar_alza_paquetes().ejecutar(crear_solicitud_paquetes())
    escritor.escribir(planes.bundle, tmp_path)
    raiz = escritor.escribir(paquetes.bundle, tmp_path)  # sin conflicto: otra carpeta

    assert b"ITEM_PRICE=68083, VENDOR_VALUE=68083" in (raiz / APLICA_PLANES).read_bytes()
    contenido = (raiz / APLICA_PAQUETES).read_bytes()
    assert b"ITEM_PRICE=11756, ITEM_PRICE_IVA=13990" in contenido
    assert contenido.count(b"\n") == contenido.count(b"\r\n")  # todo CRLF


def test_el_modulo_muestra_una_pestana_por_tipo(tmp_path: Path, qtbot: QtBot) -> None:
    widget = AlzaTarifasModule(build_context(AppPaths(base=tmp_path))).create_widget()
    qtbot.addWidget(widget)

    assert isinstance(widget, QTabWidget)
    assert [widget.tabText(i) for i in range(widget.count())] == ["Planes pospago", "Paquetes"]
    assert all(isinstance(widget.widget(i), FormularioAlzaView) for i in range(widget.count()))


def test_importa_un_excel_de_planes_con_los_titulos_de_la_tabla(tmp_path: Path) -> None:
    libro = Workbook()
    hoja = libro.active
    hoja.append(list(PLANES.formato_excel.encabezados))
    hoja.append([1208, "PLCON0335", "Pospago 5.1 Empresarial", 68083, 56320, 61950, 51246.3])
    ruta = tmp_path / "alza.xlsx"
    libro.save(ruta)

    assert LectorExcel().leer(ruta, PLANES.formato_excel) == [
        ["1208", "PLCON0335", "Pospago 5.1 Empresarial", "68083", "56320", "61950", "51246.3"]
    ]


def test_importa_un_excel_de_paquetes_con_los_titulos_de_la_tabla(tmp_path: Path) -> None:
    libro = Workbook()
    hoja = libro.active
    hoja.append(list(PAQUETES.formato_excel.encabezados))
    hoja.append(
        [28708, "SVALL2322", "Paquete Datos Corporativo 4.0 Plus", 13990, 11756, 12620, 10605.04]
    )
    ruta = tmp_path / "paquetes.xlsx"
    libro.save(ruta)

    assert LectorExcel().leer(ruta, PAQUETES.formato_excel) == [
        [
            "28708",
            "SVALL2322",
            "Paquete Datos Corporativo 4.0 Plus",
            "13990",
            "11756",
            "12620",
            "10605.04",
        ]
    ]
