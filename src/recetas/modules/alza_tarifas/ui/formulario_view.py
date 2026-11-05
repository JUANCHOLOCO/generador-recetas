"""Formulario del alza de tarifas, uno por pestaña (vista pasiva del patrón MVP)."""

from collections.abc import Sequence
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any

from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from recetas.core.domain.ambiente import Ambiente
from recetas.modules.alza_tarifas.domain.valores import MAX_AUTOR, MAX_REQUERIMIENTO
from recetas.modules.alza_tarifas.ui.formulario_presenter import DatosAlza, ErrorCampo
from recetas.modules.alza_tarifas.ui.tipos_formulario import TipoFormulario
from recetas.ui.widgets.atajos import conectar_generar
from recetas.ui.widgets.cursor import cursor_de_espera
from recetas.ui.widgets.tabla_editable import TablaEditable, TablaEditableModel


class FormularioAlzaView(QWidget):
    generar_solicitado = Signal()
    importar_solicitado = Signal(str)  # ruta del Excel elegido
    limpiar_solicitado = Signal()

    def __init__(
        self,
        tipo: TipoFormulario[Any],
        autor_sugerido: str,
        carpeta_sugerida: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._tipo = tipo
        self._titulos = [c.titulo for c in tipo.columnas]
        self._ayudas = [c.ayuda for c in tipo.columnas]
        self._fila_vacia = [""] * len(tipo.columnas)

        self._requerimiento = QLineEdit()
        self._requerimiento.setPlaceholderText("TPFB-1726")
        self._requerimiento.setMaxLength(MAX_REQUERIMIENTO)
        self._autor = QLineEdit(autor_sugerido)
        self._autor.setMaxLength(MAX_AUTOR)
        self._ambiente = QComboBox()
        for ambiente in Ambiente:
            self._ambiente.addItem(ambiente.sufijo, ambiente.value)
        self._ambiente.setCurrentIndex(self._ambiente.findData(Ambiente.PROD.value))

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
        cabecera.addRow("Carpeta de salida:", fila_carpeta)

        self._modelo = TablaEditableModel(self._titulos, self)
        self._tabla = TablaEditable(self._modelo)
        self.cargar_filas([self._fila_vacia])

        importar = QPushButton("Importar Excel…")
        importar.setProperty("variante", "secundario")
        importar.clicked.connect(self._elegir_excel)
        agregar = QPushButton("Agregar fila")
        agregar.setProperty("variante", "secundario")
        agregar.clicked.connect(self._modelo.agregar_fila)
        quitar = QPushButton("Quitar filas seleccionadas")
        quitar.setProperty("variante", "secundario")
        quitar.clicked.connect(self._quitar_seleccionadas)
        limpiar = QPushButton("Limpiar formulario")
        limpiar.setProperty("variante", "secundario")
        limpiar.clicked.connect(self.limpiar_solicitado)
        generar = QPushButton("Generar receta")
        generar.setProperty("variante", "primario")
        generar.setDefault(True)
        generar.setToolTip("Ctrl+Enter")
        generar.clicked.connect(self.generar_solicitado)
        botones = QHBoxLayout()
        botones.addWidget(importar)
        botones.addWidget(agregar)
        botones.addWidget(quitar)
        botones.addWidget(limpiar)
        botones.addStretch()
        botones.addWidget(generar)

        self._errores = QLabel()
        self._errores.setWordWrap(True)
        self._errores.setObjectName("Errores")

        titulo = QLabel(tipo.titulo)
        titulo.setObjectName("TituloTarjeta")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(titulo)
        layout.addLayout(cabecera)
        layout.addWidget(
            QLabel(
                f"{tipo.lista.capitalize()} (importe un Excel o pegue filas con Ctrl+V). "
                "Precios con coma o punto, máximo 2 decimales:"
            )
        )
        layout.addWidget(self._tabla, stretch=1)
        layout.addLayout(botones)
        layout.addWidget(self._errores)
        conectar_generar(self, self._tabla, self.generar_solicitado.emit)

    # ---------- Lo que el presenter lee ----------

    def datos(self) -> DatosAlza:
        return DatosAlza(
            requerimiento=self._requerimiento.text(),
            autor=self._autor.text(),
            ambiente=str(self._ambiente.currentData()),
            carpeta=self._carpeta.text(),
            filas=self._modelo.filas(),
        )

    # ---------- VistaAlza ----------

    def mostrar_errores(self, errores: Sequence[ErrorCampo]) -> None:
        self._modelo.marcar_errores(
            {
                (e.fila, e.columna): e.mensaje
                for e in errores
                if e.fila is not None and e.columna is not None
            }
        )
        self._errores.setText("\n".join(e.mensaje for e in errores))

    def confirmar_advertencias(self, lineas: Sequence[str]) -> bool:
        return self._preguntar(
            "Advertencias", "\n".join(lineas) + "\n\n¿Desea generar la receta de todos modos?"
        )

    def confirmar_sobrescritura(self, rutas: Sequence[str]) -> bool:
        return self._preguntar(
            "La receta ya existe", "Ya existe:\n" + "\n".join(rutas) + "\n\n¿Desea reemplazarla?"
        )

    def mostrar_resultado(self, mensaje: str) -> None:
        QMessageBox.information(self, self._tipo.titulo, mensaje)

    def mostrar_error(self, mensaje: str) -> None:
        QMessageBox.critical(self, self._tipo.titulo, mensaje)

    def confirmar_reemplazo(self, cantidad: int) -> bool:
        return self._preguntar(
            "Importar Excel",
            f"Los {cantidad} {self._tipo.lista} del Excel reemplazarán las filas del "
            "formulario. ¿Desea continuar?",
        )

    def cargar_filas(self, filas: Sequence[Sequence[str]]) -> None:
        self._modelo.cargar(self._titulos, filas, ayudas=self._ayudas)

    def confirmar_limpieza(self) -> bool:
        return self._preguntar(
            "Limpiar formulario",
            f"Se borrarán el requerimiento y los {self._tipo.lista}. ¿Desea continuar?",
        )

    def limpiar(self) -> None:
        self._requerimiento.clear()
        self.cargar_filas([self._fila_vacia])
        self.mostrar_errores([])

    def mostrar_receta_generada(self, raiz: Path) -> None:
        caja = QMessageBox(
            QMessageBox.Icon.Information,
            self._tipo.titulo,
            f"Receta generada en:\n{raiz}",
            QMessageBox.StandardButton.Ok,
            self,
        )
        abrir = caja.addButton("Abrir carpeta", QMessageBox.ButtonRole.ActionRole)
        caja.exec()
        if caja.clickedButton() is abrir:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(raiz)))

    def trabajando(self) -> AbstractContextManager[None]:
        return cursor_de_espera()

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
            self,
            f"Importar {self._tipo.lista} desde Excel",
            self._carpeta.text(),
            "Libros de Excel (*.xlsx)",
        )
        if ruta:
            self.importar_solicitado.emit(ruta)
