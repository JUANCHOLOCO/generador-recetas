"""Diálogo "Propiedades para el MOP": las líneas de cada .properties listas para copiar."""

from collections.abc import Sequence

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from recetas.modules.creacion_planes_pospago.domain.propiedades import ArchivoPropiedades

AYUDA = (
    "Copie las líneas de cada archivo en su celda del MOP. En Excel, haga doble clic en la "
    "celda (o pulse F2) antes de pegar; si no, cada línea queda en una fila distinta."
)
_LINEAS_VISIBLES = 4  # el archivo más largo (PCRFService) tiene 3, más espacio para la barra


class PropiedadesDialog(QDialog):
    def __init__(
        self, archivos: Sequence[ArchivoPropiedades], parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Propiedades para el MOP")
        self.resize(900, 640)

        ayuda = QLabel(AYUDA)
        ayuda.setWordWrap(True)

        contenido = QWidget()
        bloques = QVBoxLayout(contenido)
        for archivo in archivos:
            bloques.addWidget(self._bloque(archivo))
        bloques.addStretch()
        desplazable = QScrollArea()
        desplazable.setWidgetResizable(True)
        desplazable.setWidget(contenido)

        cerrar = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        cerrar.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(ayuda)
        layout.addWidget(desplazable, stretch=1)
        layout.addWidget(cerrar)

    def _bloque(self, archivo: ArchivoPropiedades) -> QGroupBox:
        texto = QPlainTextEdit("\n".join(archivo.lineas))
        texto.setReadOnly(True)
        texto.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        texto.setFixedHeight(texto.fontMetrics().lineSpacing() * _LINEAS_VISIBLES + 24)

        copiar = QPushButton("Copiar")
        copiar.setObjectName("Copiar")
        copiar.setProperty("variante", "secundario")
        copiar.clicked.connect(lambda: self._copiar(archivo, copiar))

        caja = QGroupBox(f"{archivo.nombre}  ·  ruta {archivo.ubicacion}")
        layout = QVBoxLayout(caja)
        layout.addWidget(texto)
        layout.addWidget(copiar, alignment=Qt.AlignmentFlag.AlignRight)
        return caja

    def _copiar(self, archivo: ArchivoPropiedades, boton: QPushButton) -> None:
        QGuiApplication.clipboard().setText("\n".join(archivo.lineas))
        boton.setText("Copiado ✓")
