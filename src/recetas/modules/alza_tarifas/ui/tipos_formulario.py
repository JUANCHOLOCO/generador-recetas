"""Lo que distingue a cada pestaña del alza: columnas de la tabla, Excel y tipo de solicitud."""

from dataclasses import dataclass

from pydantic import BaseModel

from recetas.core.domain.importacion import FormatoHoja
from recetas.modules.alza_tarifas.domain.solicitud import (
    SolicitudAlzaPaquetes,
    SolicitudAlzaPlanes,
)


@dataclass(frozen=True, slots=True)
class Columna:
    campo: str  # campo de la fila (PlanAlza o PaqueteAlza)
    titulo: str  # título en la tabla y en el Excel
    ayuda: str  # tooltip del encabezado


@dataclass(frozen=True)
class TipoFormulario[S: BaseModel]:
    pestana: str  # texto de la pestaña: "Planes pospago"
    lista: str  # campo de la solicitud con las filas y palabra de los mensajes: "planes"
    columnas: tuple[Columna, ...]
    modelo: type[S]  # solicitud que valida el formulario

    @property
    def titulo(self) -> str:
        return f"Alza de tarifas: {self.pestana.lower()}"

    @property
    def formato_excel(self) -> FormatoHoja:
        """El Excel trae los mismos títulos de la tabla en la fila 1."""
        return FormatoHoja(encabezados=tuple(c.titulo for c in self.columnas))

    def indice(self, campo: str) -> int | None:
        return next((i for i, c in enumerate(self.columnas) if c.campo == campo), None)


PLANES = TipoFormulario(
    pestana="Planes pospago",
    lista="planes",
    columnas=(
        Columna("id", "Id", "Id del plan en ACTIVATOR.PLANS (numérico, ej. 1208)"),
        Columna("part_num", "Part_num", "PLCON#### (ej. PLCON0335)"),
        Columna("nombre", "Nombre", "Nombre del plan (solo para el comentario del script)"),
        Columna("precio_nuevo", "Precio nuevo", "ITEM_PRICE y VENDOR_VALUE del aplica (ej. 68083)"),
        Columna("prorrateo_nuevo", "Prorrateo nuevo", "ITEM_PRICE_PRORRATE del aplica"),
        Columna("precio_actual", "Precio actual", "ITEM_PRICE y VENDOR_VALUE del rollback"),
        Columna("prorrateo_actual", "Prorrateo actual", "ITEM_PRICE_PRORRATE del rollback"),
    ),
    modelo=SolicitudAlzaPlanes,
)

PAQUETES = TipoFormulario(
    pestana="Paquetes",
    lista="paquetes",
    columnas=(
        Columna("id", "Id", "Id del paquete en ACTIVATOR.SERVICES (numérico, ej. 28708)"),
        Columna("part_num", "Part_num", "SVALL#### (ej. SVALL2322)"),
        Columna("nombre", "Nombre", "Nombre del paquete (solo para el comentario del script)"),
        Columna(
            "con_iva_nuevo",
            "Precio con IVA nuevo",
            "Aplica: SERVICES.ITEM_PRICE y ATP ITEM_PRICE_IVA (ej. 13990)",
        ),
        Columna("sin_iva_nuevo", "Precio sin IVA nuevo", "Aplica: ATP ITEM_PRICE (ej. 11756)"),
        Columna(
            "con_iva_actual",
            "Precio con IVA actual",
            "Rollback: SERVICES.ITEM_PRICE y ATP ITEM_PRICE_IVA",
        ),
        Columna("sin_iva_actual", "Precio sin IVA actual", "Rollback: ATP ITEM_PRICE"),
    ),
    modelo=SolicitudAlzaPaquetes,
)
