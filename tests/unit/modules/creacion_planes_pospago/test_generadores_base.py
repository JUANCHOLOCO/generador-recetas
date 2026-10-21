from datetime import date

from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.domain.scripts import CabeceraScript
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.creacion_planes_pospago.generators.base import (
    BaseSqlGenerator,
    ContextoGeneracion,
)
from tests.factories import crear_parametrizacion, crear_solicitud


class GeneradorFalso(BaseSqlGenerator):
    esquema = "ESQ"
    carpeta = "CARPETA"
    objetivo_aplica = "Aplicar"
    objetivo_rollback = "Revertir"

    def nombre_script(self, rq: str) -> str:
        return f"1_{rq}.SQL"

    def nombre_rollback(self, rq: str) -> str:
        return f"1_RB_{rq}.SQL"

    def contenido_script(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        return f"script {cab.objetivo}\n"

    def contenido_rollback(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str:
        return f"rollback {cab.objetivo}\n"


def _contexto() -> ContextoGeneracion:
    return ContextoGeneracion.crear(
        crear_solicitud(), crear_parametrizacion(), date(2026, 10, 20), "0.1.0"
    )


def test_generar_crea_los_cuatro_archivos_en_su_estructura() -> None:
    bundle = RecipeBundle("TPFB-2753")

    GeneradorFalso(JinjaRenderer("recetas.core")).generar(_contexto(), bundle)

    assert [str(f.path) for f in bundle.files] == [
        "Corriente/Script/CARPETA/ROLLBACK/1_RB_TPFB-2753_CORRIENTE.SQL",
        "Corriente/Script/CARPETA/SQL/1_TPFB-2753_CORRIENTE.SQL",
        "Corriente/Script/CARPETA/aplica-cambio.sql",
        "Corriente/Script/CARPETA/rollback-cambio.sql",
    ]
    assert bundle.get("Corriente/Script/CARPETA/SQL/1_TPFB-2753_CORRIENTE.SQL").content == (
        "script Aplicar\n"
    )


def test_el_wrapper_referencia_exactamente_el_archivo_generado() -> None:
    wrapper = GeneradorFalso(JinjaRenderer("recetas.core")).wrapper_aplica(_contexto())

    assert "@SQL/1_TPFB-2753_CORRIENTE.SQL\n" in wrapper
    assert "ALTER SESSION SET CURRENT_SCHEMA=ESQ;" in wrapper
    assert "-- AUTOR         : Equipo Tecnico" in wrapper
    assert "-- FECHA         : 20/10/2026" in wrapper
