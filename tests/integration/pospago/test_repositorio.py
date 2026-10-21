import pytest
from sqlalchemy.orm import Session, sessionmaker

from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import (
    CampoEstatico,
    Parametrizacion,
)
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan, TipoPaquete
from recetas.modules.creacion_planes_pospago.infrastructure.models import CanalModel
from recetas.modules.creacion_planes_pospago.infrastructure.repositories import (
    SqlParametrizacionRepository,
)
from recetas.modules.creacion_planes_pospago.infrastructure.seeds import (
    cargar_parametrizacion_inicial,
)

pytestmark = pytest.mark.integration


@pytest.fixture
def repo(session_factory: sessionmaker[Session]) -> SqlParametrizacionRepository:
    cargar_parametrizacion_inicial(session_factory)
    return SqlParametrizacionRepository(session_factory)


@pytest.fixture
def corriente(repo: SqlParametrizacionRepository) -> Parametrizacion:
    return repo.cargar(BillingType.CORRIENTE)


@pytest.fixture
def anticipada(repo: SqlParametrizacionRepository) -> Parametrizacion:
    return repo.cargar(BillingType.ANTICIPADA)


def test_corriente_cruza_con_nintendo_fc_y_prepago(corriente: Parametrizacion) -> None:
    nintendo = corriente.ids_de_lista(ListaCambioPlan.NINTENDO)

    assert corriente.ids_de_lista(ListaCambioPlan.PREPAGO) == ("1",)
    assert nintendo[:3] == ("7401", "7411", "7431")  # orden del Excel, no numérico
    assert len(nintendo) == 44
    assert corriente.ids_de_lista(ListaCambioPlan.CONTROL) == ()
    assert corriente.ids_de_lista(ListaCambioPlan.ATP) == ()
    assert len(corriente.ids_cambio_plan) == 45  # igual que el script Corriente de TPFB-2753


def test_anticipada_cruza_con_todas_las_listas(anticipada: Parametrizacion) -> None:
    assert anticipada.ids_de_lista(ListaCambioPlan.NINTENDO)[0] == "739"
    assert len(anticipada.ids_de_lista(ListaCambioPlan.CONTROL)) == 267  # incluye C01…P238
    assert len(anticipada.ids_de_lista(ListaCambioPlan.ATP)) == 24
    assert len(anticipada.ids_cambio_plan) == 336  # igual que el script Anticipados


def test_scoring_son_dos_listas_distintas(corriente: Parametrizacion) -> None:
    assert len(corriente.scoring_plan) == 23
    assert len(corriente.cpl_scoring_plan) == 24
    assert 18 in corriente.cpl_scoring_plan
    assert 18 not in corriente.scoring_plan


def test_campos_estaticos_de_plans(corriente: Parametrizacion) -> None:
    campos = corriente.campos("PLANS", TipoPaquete.PLAN)
    columnas = [c.columna for c in campos]

    assert len(campos) == 23
    assert CampoEstatico("PLANS", TipoPaquete.PLAN, "TYPE", "'CONTROL'") in campos
    assert "BILLING_TYPE" not in columnas


def test_planes_53_dependen_del_tipo(
    corriente: Parametrizacion, anticipada: Parametrizacion
) -> None:
    assert len(anticipada.planes_53) == 3
    assert len(corriente.planes_53) == 6


def test_listas_comunes(corriente: Parametrizacion) -> None:
    assert corriente.cadena_pool == ("LNALL0167", "SMALL0103", "PQCON0127")
    assert corriente.canales[0] == "SUB_CM"
    assert len(corriente.canales) == 16
    assert len(corriente.roles) == 241
    assert corriente.addons[0] == "SVALL2281"
    assert corriente.identify_de(TipoPaquete.SMS) == "22"


def test_filas_inactivas_se_excluyen(
    repo: SqlParametrizacionRepository, session_factory: sessionmaker[Session]
) -> None:
    with session_factory.begin() as session:
        retail = session.query(CanalModel).filter_by(nombre="Retail").one()
        retail.activo = False

    assert "Retail" not in repo.cargar(BillingType.CORRIENTE).canales
