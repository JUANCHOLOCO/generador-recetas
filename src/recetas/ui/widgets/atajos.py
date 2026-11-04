"""Atajos de teclado comunes a los formularios."""

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget

from recetas.ui.widgets.tabla_editable import TablaEditable

# Enter del teclado principal (Return) y del teclado numérico (Enter)
TECLAS_GENERAR = ("Ctrl+Return", "Ctrl+Enter")


def conectar_generar(
    formulario: QWidget, tabla: TablaEditable, generar: Callable[[], object]
) -> None:
    """Ctrl+Enter genera la receta, solo si el foco está dentro de este formulario."""

    def al_pulsar() -> None:
        tabla.confirmar_edicion()  # sin esto se perdería lo escrito en la celda abierta
        generar()

    for tecla in TECLAS_GENERAR:
        atajo = QShortcut(QKeySequence(tecla), formulario)
        atajo.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        atajo.activated.connect(al_pulsar)
