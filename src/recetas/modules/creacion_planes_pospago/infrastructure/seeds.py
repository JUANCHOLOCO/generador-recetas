"""Carga de la parametrización inicial del módulo."""

from pathlib import Path

from sqlalchemy.orm import Session, sessionmaker

from recetas.core.infrastructure.db.base import Base
from recetas.core.infrastructure.db.seeding import seed_if_empty
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

SEEDS_DIR = Path(__file__).resolve().parents[1] / "seeds"

SEEDS: tuple[tuple[type[Base], str], ...] = (
    (CplPlanPlanModel, "cpl_plan_plan.csv"),
    (ScoringModel, "scoring.csv"),
    (CanalModel, "canal.csv"),
    (CampoEstaticoModel, "campo_estatico.csv"),
    (CadenaPoolModel, "cadena_pool.csv"),
    (Plan53OldModel, "plan_53_old.csv"),
    (IdentifyModel, "identify.csv"),
    (RolModel, "rol.csv"),
    (AddonModel, "addon.csv"),
)


def cargar_parametrizacion_inicial(session_factory: sessionmaker[Session]) -> dict[str, int]:
    """Carga cada CSV en su tabla si está vacía. Devuelve filas insertadas por archivo."""
    with session_factory.begin() as session:
        return {archivo: seed_if_empty(session, model, SEEDS_DIR / archivo) for model, archivo in SEEDS}