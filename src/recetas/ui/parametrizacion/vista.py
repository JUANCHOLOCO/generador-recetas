"""Pantalla genérica de mantenimiento de tablas de parametrización (vista pasiva)."""

from collections.abc import Sequence

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from recetas.core.application.mantenimiento import ColumnaEditable, ErrorCelda
from recetas.core.domain.billing import BillingType
from recetas.ui.widgets.tabla_editable import TablaEditable, TablaEditableModel

TITULO = "Parametrización"


class ParametrizacionView(QWidget):
    tabla_elegida = Signal(int)
    filtro_cambiado = Signal(str)
    guardar_solicitado = Signal()
    recargar_solicitado = Signal()

    def __init__(self, titulos_tablas: Sequence[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._columnas: list[str] = []

        self._selector = QComboBox()
        self._selector.addItems(list(titulos_tablas))
        self._selector.currentIndexChanged.connect(self.tabla_elegida)

        self._filtro = QComboBox()
        self._filtro.addItem("Todos los tipos", "")
        for tipo in BillingType:
            self._filtro.addItem(tipo.label, tipo.value)
        self._filtro.currentIndexChanged.connect(
            lambda _: self.filtro_cambiado.emit(str(self._filtro.currentData()))
        )

        barra = QHBoxLayout()
        barra.addWidget(QLabel("Tabla:"))
        barra.addWidget(self._selector, stretch=1)
        barra.addSpacing(16)
        barra.addWidget(QLabel("Mostrar:"))
        barra.addWidget(self._filtro)

        self._modelo = TablaEditableModel([], self)
        self._tabla = TablaEditable(self._modelo)

        agregar = QPushButton("Agregar fila")
        agregar.setProperty("variante", "secundario")
        agregar.clicked.connect(self._modelo.agregar_fila)
        quitar = QPushButton("Quitar filas seleccionadas")
        quitar.setProperty("variante", "secundario")
        quitar.clicked.connect(self._quitar_seleccionadas)
        recargar = QPushButton("Recargar")
        recargar.setProperty("variante", "secundario")
        recargar.clicked.connect(self.recargar_solicitado)
        guardar = QPushButton("Guardar cambios")
        guardar.setProperty("variante", "primario")
        guardar.clicked.connect(self.guardar_solicitado)
        botones = QHBoxLayout()
        botones.addWidget(agregar)
        botones.addWidget(quitar)
        botones.addWidget(recargar)
        botones.addStretch()
        botones.addWidget(guardar)

        self._errores = QLabel()
        self._errores.setObjectName("Errores")
        self._errores.setWordWrap(True)

        titulo = QLabel(TITULO)
        titulo.setObjectName("TituloTarjeta")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(titulo)
        layout.addLayout(barra)
        layout.addWidget(
            QLabel("Pase el mouse sobre los encabezados para ver los valores permitidos.")
        )
        layout.addWidget(self._tabla, stretch=1)
        layout.addLayout(botones)
        layout.addWidget(self._errores)

    # ---------- VistaParametrizacion ----------

    def mostrar_tabla(
        self,
        columnas: Sequence[ColumnaEditable],
        filas: Sequence[list[str]],
        claves: Sequence[int | None],
    ) -> None:
        self._columnas = [c.nombre for c in columnas]
        self._modelo.cargar(
            [c.titulo for c in columnas], filas, list(claves), [c.ayuda for c in columnas]
        )
        self._tabla.resizeColumnsToContents()

    def filas(self) -> list[list[str]]:
        return self._modelo.filas()

    def claves(self) -> list[int | None]:
        return [c if isinstance(c, int) else None for c in self._modelo.claves()]

    def mostrar_solo(self, visibles: set[int] | None) -> None:
        for fila in range(self._modelo.rowCount()):
            self._tabla.setRowHidden(fila, visibles is not None and fila not in visibles)

    def seleccionar_tabla(self, indice: int) -> None:
        self._selector.blockSignals(True)
        self._selector.setCurrentIndex(indice)
        self._selector.blockSignals(False)

    def mostrar_errores(self, errores: Sequence[ErrorCelda]) -> None:
        self._modelo.marcar_errores(
            {
                (e.fila, self._columnas.index(e.columna)): e.mensaje
                for e in errores
                if e.fila is not None and e.columna in self._columnas
            }
        )
        self._errores.setText("\n".join(e.mensaje for e in errores))

    def confirmar(self, titulo: str, texto: str) -> bool:
        return QMessageBox.question(self, titulo, texto) == QMessageBox.StandardButton.Yes

    def mostrar_resultado(self, mensaje: str) -> None:
        QMessageBox.information(self, TITULO, mensaje)

    # ---------- Internos ----------

    def _quitar_seleccionadas(self) -> None:
        filas = {indice.row() for indice in self._tabla.selectionModel().selectedIndexes()}
        self._modelo.quitar_filas(sorted(filas))
