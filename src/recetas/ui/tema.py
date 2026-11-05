"""Tema visual de la aplicación: estilos e ícono (ver docs/diseno-visual.md)."""

from importlib.resources import files

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

_RECURSOS = files("recetas.ui").joinpath("resources")


def hoja_de_estilos() -> str:
    return _RECURSOS.joinpath("tema.qss").read_text(encoding="utf-8")


def icono_app() -> QIcon:
    """Ícono de la ventana y de la barra de tareas."""
    pixmap = QPixmap()
    pixmap.loadFromData(_RECURSOS.joinpath("icono.svg").read_bytes(), "SVG")
    return QIcon(pixmap)


def aplicar_tema(app: QApplication) -> None:
    app.setStyle("Fusion")
    app.setStyleSheet(hoja_de_estilos())
    app.setWindowIcon(icono_app())
