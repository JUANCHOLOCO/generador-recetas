"""Bitácora (log) de la aplicación en un archivo rotativo."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

NOMBRE = "recetas"
_FORMATO = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def configurar_bitacora(carpeta: Path) -> Path:
    """Envía los mensajes del logger 'recetas' (y sus hijos) a <carpeta>/recetas.log."""
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = (carpeta / "recetas.log").resolve()
    logger = logging.getLogger(NOMBRE)
    logger.setLevel(logging.INFO)
    ya_configurada = any(
        isinstance(h, RotatingFileHandler) and Path(h.baseFilename) == ruta
        for h in logger.handlers
    )
    if not ya_configurada:
        manejador = RotatingFileHandler(ruta, maxBytes=1_000_000, backupCount=5, encoding="utf-8")
        manejador.setFormatter(logging.Formatter(_FORMATO))
        logger.addHandler(manejador)
    return ruta


def cerrar_bitacora() -> None:
    logger = logging.getLogger(NOMBRE)
    for manejador in list(logger.handlers):
        manejador.close()
        logger.removeHandler(manejador)