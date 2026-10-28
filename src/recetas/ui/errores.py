"""Manejador global de errores inesperados: los registra y avisa al usuario."""

import logging
import sys
from collections.abc import Callable
from pathlib import Path
from types import TracebackType

from PySide6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


def _mostrar_dialogo(texto: str) -> None:
    QMessageBox.critical(None, "Error inesperado", texto)


def instalar_manejador_global(
    ruta_log: Path, mostrar: Callable[[str], None] = _mostrar_dialogo
) -> None:
    """Reemplaza sys.excepthook: todo error no controlado queda en la bitácora y se informa."""

    def manejar(
        tipo: type[BaseException], valor: BaseException, traza: TracebackType | None
    ) -> None:
        if issubclass(tipo, KeyboardInterrupt):
            sys.__excepthook__(tipo, valor, traza)
            return
        logger.critical("Error no controlado", exc_info=(tipo, valor, traza))
        mostrar(
            "Ocurrió un error inesperado y la operación no se completó.\n\n"
            f"{valor}\n\nEl detalle técnico quedó registrado en:\n{ruta_log}"
        )

    sys.excepthook = manejar