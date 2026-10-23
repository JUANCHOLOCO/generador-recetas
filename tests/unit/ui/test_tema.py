import pytest
from PySide6.QtWidgets import QApplication

from recetas.ui.tema import aplicar_tema, hoja_de_estilos

pytestmark = pytest.mark.ui


def test_la_hoja_de_estilos_viaja_con_el_paquete() -> None:
    qss = hoja_de_estilos()

    assert "QFrame#Fondo" in qss
    assert "#0A25D1" in qss


def test_aplicar_tema_configura_la_aplicacion(qapp: QApplication) -> None:
    hoja_anterior = qapp.styleSheet()
    estilo_anterior = qapp.style().name()
    try:
        aplicar_tema(qapp)

        assert qapp.styleSheet() == hoja_de_estilos()
        # Con una hoja activa, style() devuelve el envoltorio QStyleSheetStyle (sin nombre);
        # al quitarla se ve el estilo base que configuró aplicar_tema.
        qapp.setStyleSheet("")
        assert qapp.style().name().lower() == "fusion"
    finally:
        qapp.setStyle(estilo_anterior)
        qapp.setStyleSheet(hoja_anterior)
