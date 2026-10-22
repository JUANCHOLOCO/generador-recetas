"""Adaptadores SQLAlchemy de los puertos del módulo."""

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker




from recetas.core.domain.billing import BillingScope, BillingType
from recetas.core.infrastructure.db.base import ParametroMixin
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import (
    CampoEstatico,
    IdCambioPlan,
    Parametrizacion,
    Plan53,
)
from recetas.modules.creacion_planes_pospago.application.ports import PlanesRegistrados
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan, TablaScoring
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

    def registrar(self, solicitud: SolicitudReceta) -> PlanesRegistrados:
        scope = BillingScope(solicitud.tipo.value)
        vigentes = BillingScope.for_billing(solicitud.tipo)
        with self._session_factory.begin() as session:
            registrados = set(
                session.scalars(
                    select(CplPlanPlanModel.id_plan).where(
                        CplPlanPlanModel.tipo_facturacion.in_(vigentes)
                    )
                )
            )
            orden = session.scalar(select(func.max(CplPlanPlanModel.orden))) or 0
            nuevos = [p for p in solicitud.planes if p.id_plan not in registrados]
            for i, plan in enumerate(nuevos, start=1):
                session.add(
                    CplPlanPlanModel(
                        id_plan=plan.id_plan,
                        lista=ListaCambioPlan.NINTENDO,
                        orden=orden + i,
                        tipo_facturacion=scope,
                    )
                )

            registrados_53 = set(
                session.scalars(
                    select(Plan53OldModel.id_plan).where(
                        Plan53OldModel.tipo_facturacion.in_(vigentes)
                    )
                )
            )
            orden_53 = session.scalar(select(func.max(Plan53OldModel.orden))) or 0
            nuevos_53 = [p for p in solicitud.planes if p.es_53 and p.id_plan not in registrados_53]
            for i, plan in enumerate(nuevos_53, start=1):
                session.add(
                    Plan53OldModel(
                        id_plan=plan.id_plan,
                        part_num=plan.part_num,
                        orden=orden_53 + i,
                        tipo_facturacion=scope,
                    )
                )
        return PlanesRegistrados(len(nuevos), len(nuevos_53))