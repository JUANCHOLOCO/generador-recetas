"""Generadores de cada base de datos destino.

El contenido de los scripts de datos se implementa en las fases 5B (ACTIVADOR) y 5C
(SIEBEL y PROMOTIONS). Por ahora solo definen su estructura.
"""

from recetas.core.domain.scripts import CabeceraScript
from recetas.modules.creacion_planes_pospago.generators.base import (
    BaseSqlGenerator,
    ContextoGeneracion,
)


class SiebelGenerator(BaseSqlGenerator):
    esquema = "SIEBEL"
    carpeta = "SIEBEL"
    objetivo_aplica = "Actualizacion de los productos de los nuevos planes"
    objetivo_rollback = "Rollback de la actualizacion de los productos"

    def nombre_script(self, rq: str) -> str:
        return f"1_UPDATE_PRODUCTOS_{rq}_SCRIPT.SQL"

    def nombre_rollback(self, rq: str) -> str:
        return f"1_ROLLBACK_UPDATE_PRODUCTOS_{rq}_SCRIPT.SQL"

    def contenido_script(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        raise NotImplementedError("Fase 5C")

    def contenido_rollback(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        raise NotImplementedError("Fase 5C")


class PromotionsGenerator(BaseSqlGenerator):
    esquema = "PROMOTIONS"
    carpeta = "PROMOTIONS"
    objetivo_aplica = "Insercion de los nuevos planes en promociones"
    objetivo_rollback = "Rollback de los nuevos planes en promociones"

    def nombre_script(self, rq: str) -> str:
        return f"1_POID_IDENTIFY_{rq}.SQL"

    def nombre_rollback(self, rq: str) -> str:
        return f"1_PROMOTIONS_ROLLBACK_{rq}.SQL"

    def contenido_script(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        raise NotImplementedError("Fase 5C")

    def contenido_rollback(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        raise NotImplementedError("Fase 5C")
