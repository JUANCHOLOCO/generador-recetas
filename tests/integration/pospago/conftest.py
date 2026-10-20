import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from recetas.core.infrastructure.db.engine import create_session_factory


@pytest.fixture
def session_factory(engine: Engine) -> sessionmaker[Session]:
    return create_session_factory(engine)
