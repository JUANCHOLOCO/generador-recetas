from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import Engine

import recetas.modules.models  # noqa: F401
from recetas.core.infrastructure.db.base import Base
from recetas.core.infrastructure.db.migrator import upgrade_database

pytestmark = pytest.mark.integration

TABLAS_POSPAGO = {
    "pospago_cpl_plan_plan",
    "pospago_scoring",
    "pospago_canal",
    "pospago_campo_estatico",
    "pospago_cadena_pool",
    "pospago_plan_53_old",
    "pospago_identify",
    "pospago_rol",
    "pospago_addon",
}


def test_crea_las_tablas_de_parametrizacion(engine: Engine) -> None:
    tablas = set(sa.inspect(engine).get_table_names())

    assert TABLAS_POSPAGO <= tablas
    assert "alembic_version" in tablas


def test_aplicar_migraciones_dos_veces_no_falla(db_path: Path) -> None:
    upgrade_database(db_path)


def test_crea_la_carpeta_de_la_base_si_no_existe(tmp_path: Path) -> None:
    ruta = tmp_path / "no" / "existe" / "recetas.db"

    upgrade_database(ruta)

    assert ruta.is_file()


def test_las_migraciones_estan_al_dia_con_los_modelos(engine: Engine) -> None:
    with engine.connect() as connection:
        diferencias = compare_metadata(MigrationContext.configure(connection), Base.metadata)

    assert diferencias == []