"""Traducción de errores técnicos de la BD a errores de negocio con mensaje claro."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from recetas.core.domain.errors import ErrorDePersistencia

logger = logging.getLogger(__name__)


@contextmanager
def traducir_errores_de_bd(operacion: str) -> Iterator[None]:
    """Convierte cualquier error de SQLAlchemy en ErrorDePersistencia y lo registra en el log.

    IntegrityError (restricciones únicas) se deja pasar: quien llama lo traduce con más detalle.
    """
    try:
        yield
    except IntegrityError:
        raise
    except SQLAlchemyError as error:
        logger.exception("Error de base de datos al %s", operacion)
        raise ErrorDePersistencia(
            f"No se pudo {operacion}: error de la base de datos ({type(error).__name__}). "
            "Revise que no esté abierta en otro programa y que haya espacio en disco."
        ) from error