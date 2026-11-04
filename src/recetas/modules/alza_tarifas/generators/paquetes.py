"""Generador del alza de paquetes (ACTIVATOR.SERVICES y ATP_CORP_PRECIOS_SERVICE)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self

from recetas.core.application.ports import TemplateRenderer
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.domain.sql import sql_literal
from recetas.modules.alza_tarifas.domain.solicitud import PaqueteAlza, SolicitudAlzaPaquetes
from recetas.modules.alza_tarifas.domain.valores import sql_numero
from recetas.modules.alza_tarifas.generators.comun import ArmadorDeAlza, TipoAlza

PAQUETES = TipoAlza(
    carpeta="AlzaPaquetes",
    sufijo="PAQUETES",
    descripcion="paquetes",
    plantilla="alza_paquetes.sql.j2",
)


@dataclass(frozen=True, slots=True)
class FilaPaquete:
    """Un paquete ya formateado como SQL, listo para la plantilla."""

    nombre: str
    id: str
    part_num: str
    con_iva: str
    sin_iva: str

    @classmethod
    def crear(cls, paquete: PaqueteAlza, con_iva: Decimal, sin_iva: Decimal) -> Self:
        return cls(
            nombre=paquete.nombre,
            id=sql_literal(paquete.id),
            part_num=sql_literal(paquete.part_num),
            con_iva=sql_numero(con_iva),
            sin_iva=sql_numero(sin_iva),
        )


class AlzaPaquetesGenerator:
    def __init__(self, renderer: TemplateRenderer) -> None:
        self._armador = ArmadorDeAlza(renderer, PAQUETES)

    def generar(
        self, solicitud: SolicitudAlzaPaquetes, fecha: date, version: str, bundle: RecipeBundle
    ) -> None:
        paquetes = solicitud.paquetes
        self._armador.armar(
            bundle,
            requerimiento=solicitud.requerimiento,
            autor=solicitud.autor,
            fecha=fecha,
            version=version,
            nuevas=[FilaPaquete.crear(p, p.con_iva_nuevo, p.sin_iva_nuevo) for p in paquetes],
            actuales=[FilaPaquete.crear(p, p.con_iva_actual, p.sin_iva_actual) for p in paquetes],
        )
