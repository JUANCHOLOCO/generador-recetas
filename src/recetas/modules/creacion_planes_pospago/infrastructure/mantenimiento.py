"""Tablas de parametrización que el módulo expone para mantenimiento desde la app."""

from sqlalchemy.orm import Session, sessionmaker

from recetas.core.infrastructure.db.base import Base
from recetas.core.infrastructure.db.mantenimiento import SqlTablaParametrizacion
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

TABLAS: tuple[tuple[str, type[Base]], ...] = (
    ("Matriz de cambios de plan (CPL_PLAN_PLAN)", CplPlanPlanModel),
    ("Roles (CPL_ROLE_PLAN)", RolModel),
    ("Add-ons (PLAN_SERVICE)", AddonModel),
    ("Scoring", ScoringModel),
    ("Canales (SCORING_CHANNEL)", CanalModel),
    ("Campos estáticos (PLANS, SERVICES, PLAN_SERVICE)", CampoEstaticoModel),
    ("Cadena de pool (Siebel)", CadenaPoolModel),
    ("Planes 5.3 OLDS", Plan53OldModel),
    ("IDENTIFY de promociones", IdentifyModel),
)


def tablas_de_parametrizacion(
    session_factory: sessionmaker[Session],
) -> list[SqlTablaParametrizacion]:
    return [SqlTablaParametrizacion(titulo, modelo, session_factory) for titulo, modelo in TABLAS]
