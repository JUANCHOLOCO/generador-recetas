"""Creación del motor SQLite y de las sesiones."""

from pathlib import Path
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker


def sqlite_url(path: Path) -> str:
    return f"sqlite:///{path.resolve().as_posix()}"


def create_sqlite_engine(path: Path) -> Engine:
    engine = create_engine(sqlite_url(path))
    event.listen(engine, "connect", _activar_foreign_keys)
    return engine


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)


def _activar_foreign_keys(dbapi_connection: Any, _connection_record: Any) -> None:
    # SQLite trae las llaves foráneas desactivadas por defecto en cada conexión.
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
