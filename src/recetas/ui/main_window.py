"""Ventana principal. En la Fase 2 su menú se construirá desde el registro de módulos."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow

from recetas import __version__

APP_NAME = "Generador de Recetas"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} {__version__}")
        self.resize(1200, 750)

        bienvenida = QLabel("Seleccione un módulo para comenzar.")
        bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(bienvenida)
