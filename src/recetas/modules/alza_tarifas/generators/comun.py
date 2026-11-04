"""Partes comunes de los dos tipos de alza: nombres, cabeceras y los 4 archivos de ACTIVADOR."""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from recetas.core.application.ports import TemplateRenderer
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.domain.scripts import CabeceraScript

ESQUEMA = "ACTIVATOR"


@dataclass(frozen=True, slots=True)
class TipoAlza:
    carpeta: str  # carpeta propia: el alza de planes y la de paquetes del mismo RQ conviven
    sufijo: str  # nombre del script: 1_UPDATE_<RQ>_<sufijo>_SCRIPT.SQL
    descripcion: str  # objetivo de la cabecera
    plantilla: str  # recibe `cab` y `filas`


class ArmadorDeAlza:
    """Agrega al bundle los 2 lanzadores, el aplica y el rollback de un tipo de alza."""

    def __init__(self, renderer: TemplateRenderer, tipo: TipoAlza) -> None:
        self._renderer = renderer
        self._tipo = tipo

    def armar(
        self,
        bundle: RecipeBundle,
        *,
        requerimiento: str,
        autor: str,
        fecha: date,
        version: str,
        nuevas: Sequence[object],
        actuales: Sequence[object],
    ) -> None:
        tipo = self._tipo
        base = f"{tipo.carpeta}/Script/ACTIVADOR"
        script = f"1_UPDATE_{requerimiento}_{tipo.sufijo}_SCRIPT.SQL"
        rollback = f"1_ROLLBACK_UPDATE_{requerimiento}_{tipo.sufijo}_SCRIPT.SQL"

        def cabecera(objetivo: str) -> CabeceraScript:
            return CabeceraScript(
                requerimiento=requerimiento,
                objetivo=objetivo,
                base_datos=ESQUEMA,
                autor=autor,
                fecha=fecha,
                version=version,
            )

        cab_aplica = cabecera(f"Alza de tarifas de {tipo.descripcion}")
        cab_rollback = cabecera(f"Rollback del alza de tarifas de {tipo.descripcion}")
        bundle.add(f"{base}/aplica-cambio.sql", self._lanzador(cab_aplica, f"SQL/{script}"))
        bundle.add(
            f"{base}/rollback-cambio.sql", self._lanzador(cab_rollback, f"ROLLBACK/{rollback}")
        )
        bundle.add(f"{base}/SQL/{script}", self._script(cab_aplica, nuevas))
        bundle.add(f"{base}/ROLLBACK/{rollback}", self._script(cab_rollback, actuales))

    def _lanzador(self, cab: CabeceraScript, script: str) -> str:
        return self._renderer.render("wrapper.sql.j2", cab=cab, esquema=ESQUEMA, script=script)

    def _script(self, cab: CabeceraScript, filas: Sequence[object]) -> str:
        return self._renderer.render(self._tipo.plantilla, cab=cab, filas=filas)
