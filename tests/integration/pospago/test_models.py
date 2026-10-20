import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm import Session

from recetas.core.domain.billing import BillingScope
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan
from recetas.modules.creacion_planes_pospago.infrastructure.models import (
    CanalModel,
    CplPlanPlanModel,
)

pytestmark = pytest.mark.integration


def test_valores_por_defecto_ambas_y_activo(session: Session) -> None:
    session.add(CanalModel(nombre="Retail", orden=1))
    session.commit()

    canal = session.scalars(select(CanalModel)).one()

    assert canal.tipo_facturacion is BillingScope.AMBAS
    assert canal.activo is True


def test_mismo_id_plan_y_tipo_de_facturacion_no_se_repite(session: Session) -> None:
    session.add_all(
        [
            CplPlanPlanModel(
                id_plan="7391",
                lista=ListaCambioPlan.NINTENDO,
                orden=1,
                tipo_facturacion=BillingScope.CORRIENTE,
            ),
            CplPlanPlanModel(
                id_plan="7391",
                lista=ListaCambioPlan.NINTENDO,
                orden=2,
                tipo_facturacion=BillingScope.CORRIENTE,
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        session.commit()


def test_mismo_id_plan_en_distinto_tipo_si_se_permite(session: Session) -> None:
    for orden, scope in enumerate([BillingScope.CORRIENTE, BillingScope.ANTICIPADA], start=1):
        session.add(
            CplPlanPlanModel(
                id_plan="739", lista=ListaCambioPlan.NINTENDO, orden=orden, tipo_facturacion=scope
            )
        )
    session.commit()

    assert len(session.scalars(select(CplPlanPlanModel)).all()) == 2


def test_tipo_de_facturacion_desconocido_es_rechazado(session: Session) -> None:
    session.add(CanalModel(nombre="Retail", orden=1, tipo_facturacion="OTRO"))

    with pytest.raises(StatementError, match="OTRO"):
        session.commit()
