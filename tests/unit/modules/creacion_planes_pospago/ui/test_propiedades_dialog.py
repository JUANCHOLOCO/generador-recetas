import pytest
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QGroupBox, QPushButton
from pytestqt.qtbot import QtBot

from recetas.modules.creacion_planes_pospago.domain.propiedades import (
    ArchivoPropiedades,
    Ubicacion,
)
from recetas.modules.creacion_planes_pospago.ui.propiedades_dialog import PropiedadesDialog

pytestmark = pytest.mark.ui

ARCHIVOS = (
    ArchivoPropiedades("InfranetService.properties", Ubicacion.JBOSS, ("idPlansNintendo=,775",)),
    ArchivoPropiedades(
        "ussdGw.properties",
        Ubicacion.USSD,
        ("Activator.idPlansNintendo=,775", "otra=,1"),
    ),
)


def test_muestra_un_bloque_por_archivo_con_su_ruta(qtbot: QtBot) -> None:
    dialogo = PropiedadesDialog(ARCHIVOS)
    qtbot.addWidget(dialogo)

    assert [caja.title() for caja in dialogo.findChildren(QGroupBox)] == [
        "InfranetService.properties  ·  ruta %JBOSS4_PROP%",
        "ussdGw.properties  ·  ruta %USSD_PROP%",
    ]


def test_copiar_pone_solo_las_lineas_de_ese_archivo_en_el_portapapeles(qtbot: QtBot) -> None:
    dialogo = PropiedadesDialog(ARCHIVOS)
    qtbot.addWidget(dialogo)
    botones = dialogo.findChildren(QPushButton, "Copiar")

    botones[1].click()

    assert QGuiApplication.clipboard().text() == "Activator.idPlansNintendo=,775\notra=,1"
    assert botones[1].text() == "Copiado ✓"
    assert botones[0].text() == "Copiar"