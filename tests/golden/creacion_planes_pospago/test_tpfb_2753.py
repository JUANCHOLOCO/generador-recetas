"""Golden tests de TPFB-2753: salida estandarizada y equivalencia con los scripts originales."""

from datetime import date
from pathlib import Path, PurePosixPath

import pytest

from recetas.core.domain.billing import BillingType
from recetas.core.domain.recipe_bundle import RecipeBundle, RecipeFile
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.creacion_planes_pospago.generators.activador import ActivadorGenerator
from recetas.modules.creacion_planes_pospago.generators.base import (
    BaseSqlGenerator,
    ContextoGeneracion,
)
from recetas.modules.creacion_planes_pospago.generators.conf import PoolGenerator
from recetas.modules.creacion_planes_pospago.generators.scripts import (
    PromotionsGenerator,
    SiebelGenerator,
)
from tests.golden_utils import (
    Correccion,
    corregir,
    leer_original,
    reemplazar,
    sentencias,
    sentencias_sql,
    verificar_equivalencia,
    verificar_golden,
)

pytestmark = pytest.mark.golden

CASO = Path(__file__).parent / "TPFB-2753"
FECHA = date(2026, 10, 20)
VERSION = "0.1.0"
RENDERER = JinjaRenderer("recetas.modules.creacion_planes_pospago", "recetas.core")
GENERADORES = [ActivadorGenerator, SiebelGenerator, PromotionsGenerator]
TIPOS = [BillingType.CORRIENTE, BillingType.ANTICIPADA]


def a_bytes(ruta: str, contenido: str) -> bytes:
    return RecipeFile(PurePosixPath(ruta), contenido).to_bytes()


@pytest.mark.parametrize("tipo", TIPOS)
@pytest.mark.parametrize("clase", GENERADORES)
@pytest.mark.parametrize("wrapper", ["aplica-cambio.sql", "rollback-cambio.sql"])
def test_wrappers(
    tipo: BillingType,
    clase: type[BaseSqlGenerator],
    wrapper: str,
    contextos_tpfb_2753: dict[BillingType, ContextoGeneracion],
) -> None:
    ctx = contextos_tpfb_2753[tipo]
    generador = clase(RENDERER)
    texto = (
        generador.wrapper_aplica(ctx)
        if wrapper == "aplica-cambio.sql"
        else generador.wrapper_rollback(ctx)
    )
    ruta = f"{ctx.estrategia.carpeta}/Script/{generador.carpeta}/{wrapper}"

    verificar_golden(CASO / "esperado" / ruta, a_bytes(ruta, texto))
    verificar_equivalencia(sentencias(texto), sentencias(leer_original(CASO / "original" / ruta)))


@pytest.mark.parametrize("tipo", TIPOS)
def test_pool(
    tipo: BillingType, contextos_tpfb_2753: dict[BillingType, ContextoGeneracion]
) -> None:
    ctx = contextos_tpfb_2753[tipo]
    bundle = RecipeBundle("TPFB-2753")

    PoolGenerator().generar(ctx, bundle)

    [archivo] = bundle.files
    ruta = str(archivo.path)
    verificar_golden(CASO / "esperado" / ruta, archivo.to_bytes())
    assert archivo.to_bytes() == (CASO / "original" / ruta).read_bytes()


# Correcciones intencionales del estándar (docs/estandar-scripts.md §6 y §7).
CORRECCIONES_ACTIVADOR_ROLLBACK: list[Correccion] = [
    reemplazar("FROM SCORING_PLAN WHERE", "FROM ACTIVATOR.SCORING_PLAN WHERE"),  # #7: esquema
    reemplazar("FROM SERVICES S WHERE", "FROM ACTIVATOR.SERVICES S WHERE"),  # #7: esquema
]


@pytest.mark.parametrize("tipo", TIPOS)
@pytest.mark.parametrize("carpeta", ["SQL", "ROLLBACK"])
def test_activador(
    contextos_tpfb_2753: dict[BillingType, ContextoGeneracion],
    tipo: BillingType,
    carpeta: str,
) -> None:
    ctx = contextos_tpfb_2753[tipo]
    generador = ActivadorGenerator(RENDERER)
    if carpeta == "SQL":
        nombre = generador.nombre_script(ctx.rq)
        texto = generador.contenido_script(ctx, generador.cabecera(ctx, generador.objetivo_aplica))
        correcciones: list[Correccion] = []
    else:
        nombre = generador.nombre_rollback(ctx.rq)
        texto = generador.contenido_rollback(
            ctx, generador.cabecera(ctx, generador.objetivo_rollback)
        )
        correcciones = CORRECCIONES_ACTIVADOR_ROLLBACK
    ruta = f"{ctx.estrategia.carpeta}/Script/{generador.carpeta}/{carpeta}/{nombre}"

    verificar_golden(CASO / "esperado" / ruta, a_bytes(ruta, texto))
    original = sentencias_sql(leer_original(CASO / "original" / ruta))
    verificar_equivalencia(sentencias_sql(texto), corregir(original, correcciones))
