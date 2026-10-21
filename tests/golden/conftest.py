import json
from datetime import date
from pathlib import Path

import pytest

from recetas.core.domain.billing import BillingType
from recetas.core.infrastructure.db.engine import create_session_factory, create_sqlite_engine
from recetas.core.infrastructure.db.migrator import upgrade_database
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta
from recetas.modules.creacion_planes_pospago.generators.base import ContextoGeneracion
from recetas.modules.creacion_planes_pospago.infrastructure.repositories import (
    SqlParametrizacionRepository,
)
from recetas.modules.creacion_planes_pospago.infrastructure.seeds import (
    cargar_parametrizacion_inicial,
)

CASO_TPFB_2753 = Path(__file__).parent / "creacion_planes_pospago" / "TPFB-2753"


@pytest.fixture(scope="session")
def contextos_tpfb_2753(
    tmp_path_factory: pytest.TempPathFactory,
) -> dict[BillingType, ContextoGeneracion]:
    """Solicitudes de TPFB-2753 con la parametrización real de los seeds, por tipo."""
    db = tmp_path_factory.mktemp("golden") / "golden.db"
    upgrade_database(db)
    engine = create_sqlite_engine(db)
    try:
        session_factory = create_session_factory(engine)
        cargar_parametrizacion_inicial(session_factory)
        repo = SqlParametrizacionRepository(session_factory)
        contextos = {}
        for tipo in BillingType:
            entrada = CASO_TPFB_2753 / f"entrada_{tipo.value.lower()}.json"
            solicitud = SolicitudReceta.model_validate(
                json.loads(entrada.read_text(encoding="utf-8"))
            )
            contextos[tipo] = ContextoGeneracion.crear(
                solicitud, repo.cargar(tipo), date(2026, 10, 20), "0.1.0"
            )
        return contextos
    finally:
        engine.dispose()
