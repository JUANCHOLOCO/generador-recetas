import pytest
from sqlalchemy.orm import Session, sessionmaker

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.application.ports import PlanesRegistrados
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan
from recetas.modules.creacion_planes_pospago.infrastructure.repositories import (
    SqlParametrizacionRepository,
)
from recetas.modules.creacion_planes_pospago.infrastructure.seeds import (
    cargar_parametrizacion_inicial,
)
from tests.factories import crear_solicitud, datos_plan

pytestmark = pytest.mark.integration


@pytest.fixture
def repo(session_factory: sessionmaker[Session]) -> SqlParametrizacionRepository:
    cargar_parametrizacion_inicial(session_factory)
    return SqlParametrizacionRepository(session_factory)


def test_planes_ya_registrados_no_se_duplican(repo: SqlParametrizacionRepository) -> None:
    # 7751 (plan 5.1 FC de TPFB-2753) ya viene en los seeds de Corriente.
    assert repo.registrar(crear_solicitud()) == PlanesRegistrados(cambio_plan=0, planes_53=0)


def test_plan_nuevo_queda_al_final_de_nintendo_solo_para_su_tipo(
    repo: SqlParametrizacionRepository,
) -> None:
    solicitud = crear_solicitud(planes=[datos_plan(id_plan="7999", es_53=True)])

    resultado = repo.registrar(solicitud)

    corriente = repo.cargar(BillingType.CORRIENTE)
    anticipada = repo.cargar(BillingType.ANTICIPADA)
    assert resultado == PlanesRegistrados(cambio_plan=1, planes_53=1)
    assert corriente.ids_de_lista(ListaCambioPlan.NINTENDO)[-1] == "7999"
    assert "7999" not in anticipada.ids_de_lista(ListaCambioPlan.NINTENDO)
    assert corriente.planes_53[-1].id_plan == "7999"


def test_registrar_dos_veces_es_idempotente(repo: SqlParametrizacionRepository) -> None:
    solicitud = crear_solicitud(planes=[datos_plan(id_plan="7999")])
    repo.registrar(solicitud)

    assert repo.registrar(solicitud) == PlanesRegistrados(cambio_plan=0, planes_53=0)