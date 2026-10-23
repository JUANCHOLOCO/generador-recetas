"""Tema visual de la aplicación (ver docs/diseno-visual.md)."""

from importlib.resources import files

from PySide6.QtWidgets import QApplication


def hoja_de_estilos() -> str:
    return files("recetas.ui").joinpath("resources/tema.qss").read_text(encoding="utf-8")


def aplicar_tema(app: QApplication) -> None:
    app.setStyle("Fusion")
    app.setStyleSheet(hoja_de_estilos())
