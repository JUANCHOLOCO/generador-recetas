from pathlib import Path

import pytest
from PySide6.QtWidgets import QTabWidget
from pytestqt.qtbot import QtBot

from recetas.config import AppPaths
from recetas.main import build_context
from recetas.modules.creacion_planes_pospago.module import CreacionPlanesPospagoModule
from recetas.modules.creacion_planes_pospago.ui.formulario_view import FormularioView
from tests.factories import crear_solicitud

pytestmark = pytest.mark.integration


def test_el_modulo_genera_una_receta_con_dependencias_reales(tmp_path: Path) -> None:
    modulo = CreacionPlanesPospagoModule(build_context(AppPaths(base=tmp_path)))
    modulo.initialize()

    receta = modulo.generar_receta().ejecutar(crear_solicitud())

    assert str(receta.bundle.root) == "TPFB-2753_Prod"
    assert len(receta.bundle) == 13


def test_el_modulo_muestra_el_formulario(tmp_path: Path, qtbot: QtBot) -> None:
    modulo = CreacionPlanesPospagoModule(build_context(AppPaths(base=tmp_path)))

    widget = modulo.create_widget()
    qtbot.addWidget(widget)

    assert isinstance(widget, QTabWidget)
    assert widget.tabText(0) == "Generar receta"
    assert isinstance(widget.widget(0), FormularioView)
