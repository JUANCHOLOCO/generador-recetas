"""Cursor de espera mientras la app trabaja (generar o escribir recetas grandes)."""

from collections.abc import Iterator
from contextlib import contextmanager

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication


@contextmanager
def cursor_de_espera() -> Iterator[None]:
    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
    try:
        yield
    finally:
        QApplication.restoreOverrideCursor()  # también si hubo un error
