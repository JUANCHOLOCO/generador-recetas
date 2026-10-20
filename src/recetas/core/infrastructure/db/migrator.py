"""Aplica las migraciones Alembic pendientes sobre la base SQLite."""

from pathlib import Path

from alembic import command
from alembic.config import Config

from recetas.core.infrastructure.db.engine import sqlite_url

MIGRATIONS_DIR = Path(__file__).resolve().parents[3] / "migrations"


def upgrade_database(db_path: Path) -> None:
    """Crea la base si no existe y la deja en la última versión del esquema."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    config = Config()
    config.set_main_option("script_location", str(MIGRATIONS_DIR))
    config.set_main_option("sqlalchemy.url", sqlite_url(db_path))
    command.upgrade(config, "head")
