"""Formulario de creación de planes Pospago (vista pasiva del patrón MVP)."""

from collections.abc import Sequence

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from recetas.core.domain.ambiente import Ambiente
from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.advertencias import Advertencia
from recetas.modules.creacion_planes_pospago.domain.propiedades import ArchivoPropiedades
from recetas.modules.creacion_planes_pospago.domain.valores import MAX_AUTOR, MAX_REQUERIMIENTO
from recetas.modules.creacion_planes_pospago.ui.formulario_presenter import (
    COLUMNAS,
    DatosFormulario,
    ErrorCampo,
)
from recetas.modules.creacion_planes_pospago.ui.propiedades_dialog import PropiedadesDialog
from recetas.ui.widgets.tabla_editable import TablaEditable, TablaEditableModel

TITULO = "Creación de planes Pospago"


class FormularioView(QWidget):
    generar_solicitado = Signal()
    importar_solicitado = Signal(str)  # ruta del Excel elegido
    tipo_cambiado = Signal()

    def __init__(
        self, autor_sugerido: str, carpeta_sugerida: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        self._requerimiento = QLineEdit()
        self._requerimiento.setPlaceholderText("TPFB-2753")
        self._requerimiento.setMaxLength(MAX_REQUERIMIENTO)
        self._autor = QLineEdit(autor_sugerido)
        self._autor.setMaxLength(MAX_AUTOR)
        self._ambiente = QComboBox()
        for ambiente in Ambiente:
            self._ambiente.addItem(ambiente.sufijo, ambiente.value)
        self._ambiente.setCurrentIndex(self._ambiente.findData(Ambiente.PROD.value))

        self._corriente = QRadioButton(BillingType.CORRIENTE.label)
        self._anticipada = QRadioButton(BillingType.ANTICIPADA.label)
        self._tipos = QButtonGroup(self)
        tipos = QButtonGroup(self)
        self._tipos.addButton(self._corriente)
        self._tipos.addButton(self._anticipada)
        self._tipos.buttonClicked.connect(lambda _boton: self.tipo_cambiado.emit())
        fila_tipos = QHBoxLayout()
        fila_tipos.addWidget(self._corriente)
        fila_tipos.addWidget(self._anticipada)
        fila_tipos.addStretch()

        self._carpeta = QLineEdit(carpeta_sugerida)
        examinar = QPushButton("Examinar…")
        examinar.setProperty("variante", "secundario")
        examinar.clicked.connect(self._elegir_carpeta)
        fila_carpeta = QHBoxLayout()
        fila_carpeta.addWidget(self._carpeta)
        fila_carpeta.addWidget(examinar)

        cabecera = QFormLayout()
        cabecera.addRow("Número de requerimiento:", self._requerimiento)
        cabecera.addRow("Autor:", self._autor)
        cabecera.addRow("Ambiente:", self._ambiente)
        cabecera.addRow("Tipo de facturación:", fila_tipos)
        cabecera.addRow("Carpeta de salida:", fila_carpeta)

        self._modelo = TablaEditableModel([c.titulo for c in COLUMNAS], self)
        self._modelo.agregar_fila()
        self._tabla = TablaEditable(self._modelo)

        agregar = QPushButton("Agregar fila")
        agregar.setProperty("variante", "secundario")
        agregar.clicked.connect(self._modelo.agregar_fila)
        quitar = QPushButton("Quitar filas seleccionadas")
        quitar.setProperty("variante", "secundario")
        quitar.clicked.connect(self._quitar_seleccionadas)
        generar = QPushButton("Generar receta")
        generar.setProperty("variante", "primario")
        generar.setDefault(True)
        generar.clicked.connect(self.generar_solicitado)
        importar = QPushButton("Importar Excel…")
        importar.setProperty("variante", "secundario")
        importar.clicked.connect(self._elegir_excel)
        botones = QHBoxLayout()
        botones.addWidget(importar)
        botones.addWidget(agregar)
        botones.addWidget(quitar)
        botones.addStretch()
        botones.addWidget(generar)

        self._errores = QLabel()
        self._errores.setWordWrap(True)
        self._errores.setObjectName("Errores")

        self._avisos = QLabel()
        self._avisos.setWordWrap(True)
        self._avisos.setObjectName("Avisos")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel(TITULO)
        titulo.setObjectName("TituloTarjeta")
        layout.addWidget(titulo)
        layout.addLayout(cabecera)
        layout.addWidget(
            QLabel("Planes (importe un Excel o pegue filas copiadas de Excel con Ctrl+V):")
        )
        layout.addWidget(self._tabla, stretch=1)
        layout.addLayout(botones)
        layout.addWidget(self._avisos)
        layout.addWidget(self._errores)

    # ---------- Lo que el presenter lee ----------

    def datos(self) -> DatosFormulario:
        if self._corriente.isChecked():
            tipo = BillingType.CORRIENTE.value
        elif self._anticipada.isChecked():
            tipo = BillingType.ANTICIPADA.value
        else:
            tipo = ""
        return DatosFormulario(
            requerimiento=self._requerimiento.text(),
            autor=self._autor.text(),
            ambiente=str(self._ambiente.currentData()),
            tipo=tipo,
            carpeta=self._carpeta.text(),
            filas=self._modelo.filas(),
        )

    # ---------- VistaFormulario ----------

    def mostrar_errores(self, errores: Sequence[ErrorCampo]) -> None:
        self._modelo.marcar_errores(
            {
                (e.fila, e.columna): e.mensaje
                for e in errores
                if e.fila is not None and e.columna is not None
            }
        )
        self._errores.setText("\n".join(e.mensaje for e in errores))

    def confirmar_advertencias(self, advertencias: Sequence[Advertencia]) -> bool:
        lineas = [f"Fila {a.fila}: {a.mensaje}" if a.fila else a.mensaje for a in advertencias]
        return self._preguntar(
            "Advertencias", "\n".join(lineas) + "\n\n¿Desea generar la receta de todos modos?"
        )

    def confirmar_sobrescritura(self, rutas: Sequence[str]) -> bool:
        return self._preguntar(
            "La receta ya existe", "Ya existe:\n" + "\n".join(rutas) + "\n\n¿Desea reemplazarla?"
        )

    def confirmar_registro(self, cantidad: int) -> bool:
        return self._preguntar(
            "Registrar planes",
            f"¿Registrar los {cantidad} planes en la parametrización para los próximos "
            "requerimientos?",
        )

    def mostrar_resultado(self, mensaje: str) -> None:
        QMessageBox.information(self, TITULO, mensaje)

    def mostrar_propiedades(self, archivos: Sequence[ArchivoPropiedades]) -> None:
        PropiedadesDialog(archivos, self).exec()

    def mostrar_error(self, mensaje: str) -> None:
        QMessageBox.critical(self, TITULO, mensaje)

    def confirmar_reemplazo(self, cantidad: int) -> bool:
        return self._preguntar(
            "Importar Excel",
            f"Los {cantidad} planes del Excel reemplazarán las filas del formulario. "
            "¿Desea continuar?",
        )

    def cargar_planes(self, filas: Sequence[Sequence[str]]) -> None:
        self._modelo.cargar([c.titulo for c in COLUMNAS], filas)

    def mostrar_avisos(self, avisos: Sequence[str]) -> None:
        self._avisos.setText("\n".join(avisos))

    # ---------- Internos ----------

    def _preguntar(self, titulo: str, texto: str) -> bool:
        return QMessageBox.question(self, titulo, texto) == QMessageBox.StandardButton.Yes

    def _elegir_carpeta(self) -> None:
        carpeta = QFileDialog.getExistingDirectory(self, "Carpeta de salida", self._carpeta.text())
        if carpeta:
            self._carpeta.setText(carpeta)

    def _quitar_seleccionadas(self) -> None:
        filas = {indice.row() for indice in self._tabla.selectionModel().selectedIndexes()}
        self._modelo.quitar_filas(sorted(filas))

    def _elegir_excel(self) -> None:
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Importar planes desde Excel", self._carpeta.text(), "Libros de Excel (*.xlsx)"
        )
        if ruta:
            self.importar_solicitado.emit(ruta)
