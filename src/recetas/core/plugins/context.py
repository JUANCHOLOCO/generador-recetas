"""Dependencias compartidas que la aplicación entrega a cada módulo."""

from dataclasses import dataclass

from sqlalchemy.orm import Session, sessionmaker

from recetas.config import AppPaths
from recetas.core.application.ports import Reloj, UsuarioActual


@dataclass(frozen=True, slots=True)
class AppContext:
    paths: AppPaths
    session_factory: sessionmaker[Session]
    reloj: Reloj
    usuario: UsuarioActual
