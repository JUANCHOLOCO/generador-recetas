"""Tablas de parametrización del módulo (antes hoja 'Reglas Aplicabilidad')."""

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from recetas.core.infrastructure.db.base import Base, ParametroMixin, enum_type
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan, TipoPaquete


class CplPlanPlanModel(ParametroMixin, Base):
    """IDs con los que se cruza un plan nuevo en la matriz de cambios de plan."""

    __tablename__ = "pospago_cpl_plan_plan"
    __table_args__ = (UniqueConstraint("id_plan", "tipo_facturacion"),)

    id_plan: Mapped[str] = mapped_column(String(20))
    lista: Mapped[ListaCambioPlan] = mapped_column(enum_type(ListaCambioPlan))


class ScoringModel(ParametroMixin, Base):
    """IDs para SCORING_PLAN (id_scor) y CPL_SCORING_PLAN (scoring_id)."""

    __tablename__ = "pospago_scoring"
    __table_args__ = (UniqueConstraint("id_scor", "tipo_facturacion"),)

    id_scor: Mapped[int]
    scoring_id: Mapped[int]


class CanalModel(ParametroMixin, Base):
    """Canales del cursor de ACTIVATOR.scoring_channel."""

    __tablename__ = "pospago_canal"
    __table_args__ = (UniqueConstraint("nombre", "tipo_facturacion"),)

    nombre: Mapped[str] = mapped_column(String(50))


class CampoEstaticoModel(ParametroMixin, Base):
    """Valor fijo de una columna en PLANS, SERVICES o PLAN_SERVICE."""

    __tablename__ = "pospago_campo_estatico"
    __table_args__ = (UniqueConstraint("tabla", "tipo_paquete", "columna", "tipo_facturacion"),)

    tabla: Mapped[str] = mapped_column(String(30))
    tipo_paquete: Mapped[TipoPaquete] = mapped_column(enum_type(TipoPaquete))
    columna: Mapped[str] = mapped_column(String(50))
    valor_sql: Mapped[str] = mapped_column(String(200))


class CadenaPoolModel(ParametroMixin, Base):
    """Part nums fijos al inicio de la cadena de pool de Siebel."""

    __tablename__ = "pospago_cadena_pool"
    __table_args__ = (UniqueConstraint("part_num", "tipo_facturacion"),)

    part_num: Mapped[str] = mapped_column(String(20))


class Plan53OldModel(ParametroMixin, Base):
    """Planes con comportamiento 5.3."""

    __tablename__ = "pospago_plan_53_old"
    __table_args__ = (UniqueConstraint("id_plan", "tipo_facturacion"),)

    id_plan: Mapped[str] = mapped_column(String(20))
    part_num: Mapped[str] = mapped_column(String(20))


class IdentifyModel(ParametroMixin, Base):
    """IDENTIFY de PROMOTIONS por tipo de paquete (plan=21, SMS=22, datos=23)."""

    __tablename__ = "pospago_identify"
    __table_args__ = (UniqueConstraint("tipo_paquete", "tipo_facturacion"),)

    tipo_paquete: Mapped[TipoPaquete] = mapped_column(enum_type(TipoPaquete))
    identify: Mapped[str] = mapped_column(String(10))


class RolModel(ParametroMixin, Base):
    """Perfiles que pueden ver los planes nuevos (CPL_ROLE_PLAN)."""

    __tablename__ = "pospago_rol"
    __table_args__ = (UniqueConstraint("role_granted", "tipo_facturacion"),)

    role_granted: Mapped[str] = mapped_column(String(50))


class AddonModel(ParametroMixin, Base):
    """Part nums de add-ons existentes que se asocian a cada plan (PLAN_SERVICE)."""

    __tablename__ = "pospago_addon"
    __table_args__ = (UniqueConstraint("part_num", "tipo_facturacion"),)

    part_num: Mapped[str] = mapped_column(String(20))
