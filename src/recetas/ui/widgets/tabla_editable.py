"""Tabla tipo hoja de cálculo: edición, pegado desde Excel y errores marcados por celda."""

from collections.abc import Mapping, Sequence
from typing import override

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QObject, QPersistentModelIndex, Qt
from PySide6.QtGui import QBrush, QColor, QGuiApplication, QKeyEvent, QKeySequence
from PySide6.QtWidgets import QTableView, QWidget

Indice = QModelIndex | QPersistentModelIndex
Celda = tuple[int, int]

_COLOR_ERROR = QColor("#f8d7da")


class TablaEditableModel(QAbstractTableModel):
    def __init__(self, titulos: Sequence[str], parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._titulos = list(titulos)
        self._filas: list[list[str]] = []
        self._errores: dict[Celda, str] = {}

    # ---------- Contrato de Qt ----------
    @override
    def rowCount(self, parent: Indice | None = None) -> int:
        return 0 if parent is not None and parent.isValid() else len(self._filas)
    @override
    def columnCount(self, parent: Indice | None = None) -> int:
        return 0 if parent is not None and parent.isValid() else len(self._titulos)
    @override
    def data(self, index: Indice, role: int = Qt.ItemDataRole.DisplayRole) -> object:
        if not index.isValid():
            return None
        celda = (index.row(), index.column())
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return self._filas[index.row()][index.column()]
        if role == Qt.ItemDataRole.BackgroundRole and celda in self._errores:
            return QBrush(_COLOR_ERROR)
        if role == Qt.ItemDataRole.ToolTipRole:
            return self._errores.get(celda)
        return None
    @override
    def setData(self, index: Indice, value: object, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
        self._filas[index.row()][index.column()] = str(value).strip()
        self._errores.pop((index.row(), index.column()), None)
        self.dataChanged.emit(index, index)
        return True
    @override
    def flags(self, index: Indice) -> Qt.ItemFlag:
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable
    @override
    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ) -> object:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self._titulos[section]
        return str(section + 1)

    # ---------- API propia ----------

    def filas(self) -> list[list[str]]:
        return [fila.copy() for fila in self._filas]

    def agregar_fila(self) -> None:
        n = len(self._filas)
        self.beginInsertRows(QModelIndex(), n, n)
        self._filas.append([""] * len(self._titulos))
        self.endInsertRows()

    def quitar_filas(self, filas: Sequence[int]) -> None:
        for fila in sorted(set(filas), reverse=True):
            self.beginRemoveRows(QModelIndex(), fila, fila)
            del self._filas[fila]
            self.endRemoveRows()
        self.marcar_errores({})

    def pegar(self, texto: str, fila: int = 0, columna: int = 0) -> int:
        """Pega texto separado por tabuladores (formato de Excel). Devuelve las filas pegadas."""
        lineas = [linea for linea in texto.replace("\r\n", "\n").split("\n") if linea.strip()]
        for i, linea in enumerate(lineas):
            while fila + i >= len(self._filas):
                self.agregar_fila()
            for j, valor in enumerate(linea.split("\t")):
                if columna + j < len(self._titulos):
                    self._filas[fila + i][columna + j] = valor.strip()
        self.marcar_errores({})
        return len(lineas)

    def marcar_errores(self, errores: Mapping[Celda, str]) -> None:
        self._errores = dict(errores)
        if self._filas:
            ultima = self.index(len(self._filas) - 1, len(self._titulos) - 1)
            self.dataChanged.emit(self.index(0, 0), ultima)

@override
class TablaEditable(QTableView):
    """Vista de la tabla que entiende Ctrl+V con datos copiados de Excel."""

    def __init__(self, modelo: TablaEditableModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._modelo = modelo
        self.setModel(modelo)
        self.horizontalHeader().setStretchLastSection(True)
    @override
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.matches(QKeySequence.StandardKey.Paste):
            actual = self.currentIndex()
            texto = QGuiApplication.clipboard().text()
            self._modelo.pegar(texto, max(actual.row(), 0), max(actual.column(), 0))
            return
        super().keyPressEvent(event)
