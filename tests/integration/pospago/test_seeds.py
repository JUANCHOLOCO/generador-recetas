import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from recetas.modules.creacion_planes_pospago.infrastructure.models import CanalModel
from recetas.modules.creacion_planes_pospago.infrastructure.seeds import (
    cargar_parametrizacion_inicial,
)

pytestmark = pytest.mark.integration

FILAS_ESPERADAS = {
    "cpl_plan_plan.csv": 334,
    "scoring.csv": 47,
    "canal.csv": 16,
    "campo_estatico.csv": 66,
    "cadena_pool.csv": 3,
    "plan_53_old.csv": 6,
    "identify.csv": 3,
    "rol.csv": 241,
    "addon.csv": 12,
}


def test_primera_carga_inserta_todos_los_seeds(session_factory: sessionmaker[Session]) -> None:
    assert cargar_parametrizacion_inicial(session_factory) == FILAS_ESPERADAS


def test_segunda_carga_no_duplica(session_factory: sessionmaker[Session]) -> None:
    cargar_parametrizacion_inicial(session_factory)

    segunda = cargar_parametrizacion_inicial(session_factory)

    assert set(segunda.values()) == {0}


def test_no_sobrescribe_una_tabla_que_el_usuario_ya_modifico(
    session_factory: sessionmaker[Session],
) -> None:
    with session_factory.begin() as session:
        session.add(CanalModel(nombre="Canal propio", orden=1))

    resultado = cargar_parametrizacion_inicial(session_factory)

    assert resultado["canal.csv"] == 0
    with session_factory() as session:
        assert session.scalars(select(CanalModel.nombre)).all() == ["Canal propio"]