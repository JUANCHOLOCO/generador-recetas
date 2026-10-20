"""Base declarativa de SQLAlchemy compartida por todos los módulos."""

from enum import StrEnum

from sqlalchemy import Enum, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from recetas.core.domain.billing import BillingScope

# Nombres deterministas para restricciones: Alembic los necesita para poder
# modificarlas después en SQLite.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def enum_type(enum_cls: type[StrEnum]) -> Enum:
    """Guarda un StrEnum como texto (VARCHAR) y rechaza valores desconocidos."""
    return Enum(enum_cls, native_enum=False, length=20, validate_strings=True)


class ParametroMixin:
    """Columnas comunes a toda tabla de parametrización."""

    id: Mapped[int] = mapped_column(primary_key=True)
    orden: Mapped[int]
    tipo_facturacion: Mapped[BillingScope] = mapped_column(
        enum_type(BillingScope), default=BillingScope.AMBAS
    )
    activo: Mapped[bool] = mapped_column(default=True)
