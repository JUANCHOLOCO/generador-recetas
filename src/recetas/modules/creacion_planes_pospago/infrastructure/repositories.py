"""Adaptadores SQLAlchemy de los puertos del módulo."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from recetas.core.domain.billing import BillingScope, BillingType
from recetas.core.infrastructure.db.base import ParametroMixin
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import (
    CampoEstatico,
    IdCambioPlan,
    Parametrizacion,
    Plan53,
)
from recetas.modules.creacion_planes_pospago.domain.tipos import TablaScoring
from recetas.modules.creacion_planes_pospago.infrastructure.models import (
    AddonModel,
    CadenaPoolModel,
    CampoEstaticoModel,
    CanalModel,
    CplPlanPlanModel,
    IdentifyModel,
    Plan53OldModel,
    RolModel,
    ScoringModel,
)


class SqlParametrizacionRepository:
    """Implementa ParametrizacionRepository sobre las tablas pospago_*."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def cargar(self, tipo: BillingType) -> Parametrizacion:
        scopes = BillingScope.for_billing(tipo)

        with self._session_factory() as session:

            def activos[M: ParametroMixin](model: type[M]) -> Sequence[M]:
                consulta = (
                    select(model)
                    .where(model.activo.is_(True), model.tipo_facturacion.in_(scopes))
                    .order_by(model.orden, model.id)
                )
                return session.scalars(consulta).all()

            scoring = activos(ScoringModel)
            return Parametrizacion(
                tipo=tipo,
                ids_cambio_plan=tuple(
                    IdCambioPlan(f.id_plan, f.lista) for f in activos(CplPlanPlanModel)
                ),
                scoring_plan=tuple(
                    f.scoring_id for f in scoring if f.tabla_destino is TablaScoring.SCORING_PLAN
                ),
                cpl_scoring_plan=tuple(
                    f.scoring_id
                    for f in scoring
                    if f.tabla_destino is TablaScoring.CPL_SCORING_PLAN
                ),
                canales=tuple(f.nombre for f in activos(CanalModel)),
                campos_estaticos=tuple(
                    CampoEstatico(f.tabla, f.tipo_paquete, f.columna, f.valor_sql)
                    for f in activos(CampoEstaticoModel)
                ),
                cadena_pool=tuple(f.part_num for f in activos(CadenaPoolModel)),
                planes_53=tuple(Plan53(f.id_plan, f.part_num) for f in activos(Plan53OldModel)),
                identify={f.tipo_paquete: f.identify for f in activos(IdentifyModel)},
                roles=tuple(f.role_granted for f in activos(RolModel)),
                addons=tuple(f.part_num for f in activos(AddonModel)),
            )