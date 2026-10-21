"""Golden tests de TPFB-2753: salida estandarizada y equivalencia con los scripts originales."""

import json
from datetime import date
from pathlib import Path, PurePosixPath

import pytest

from recetas.core.domain.billing import BillingType
from recetas.core.domain.recipe_bundle import RecipeBundle, RecipeFile
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta
from recetas.modules.creacion_planes_pospago.generators.base import (
    BaseSqlGenerator,
    ContextoGeneracion,
)
from recetas.modules.creacion_planes_pospago.generators.conf import PoolGenerator
from recetas.modules.creacion_planes_pospago.generators.scripts import (
    ActivadorGenerator,
    PromotionsGenerator,
    SiebelGenerator,
)
from tests.factories import crear_parametrizacion
from tests.golden_utils import leer_original, sentencias, verificar_golden

pytestmark = pytest.mark.golden

CASO = Path(__file__).parent / "TPFB-2753"
FECHA = date(2026, 10, 20)
VERSION = "0.1.0"
RENDERER = JinjaRenderer("recetas.modules.creacion_planes_pospago", "recetas.core")
GENERADORES = [ActivadorGenerator, SiebelGenerator, PromotionsGenerator]
TIPOS = [BillingType.CORRIENTE, BillingType.ANTICIPADA]


def contexto(tipo: BillingType) -> ContextoGeneracion:
    archivo = CASO / f"entrada_{tipo.value.lower()}.json"
    solicitud = SolicitudReceta.model_validate(json.loads(archivo.read_text(encoding="utf-8")))
    return ContextoGeneracion.crear(solicitud, crear_parametrizacion(tipo=tipo), FECHA, VERSION)


def a_bytes(ruta: str, contenido: str) -> bytes:
    return RecipeFile(PurePosixPath(ruta), contenido).to_bytes()


@pytest.mark.parametrize("tipo", TIPOS)
@pytest.mark.parametrize("clase", GENERADORES)
@pytest.mark.parametrize("wrapper", ["aplica-cambio.sql", "rollback-cambio.sql"])
def test_wrappers(tipo: BillingType, clase: type[BaseSqlGenerator], wrapper: str) -> None:
    ctx = contexto(tipo)
    generador = clase(RENDERER)
    texto = (
        generador.wrapper_aplica(ctx)
        if wrapper == "aplica-cambio.sql"
        else generador.wrapper_rollback(ctx)
    )
    ruta = f"{ctx.estrategia.carpeta}/Script/{generador.carpeta}/{wrapper}"

    verificar_golden(CASO / "esperado" / ruta, a_bytes(ruta, texto))
    assert sentencias(texto) == sentencias(leer_original(CASO / "original" / ruta))


@pytest.mark.parametrize("tipo", TIPOS)
def test_pool(tipo: BillingType) -> None:
    ctx = contexto(tipo)
    bundle = RecipeBundle("TPFB-2753")

    PoolGenerator().generar(ctx, bundle)

    [archivo] = bundle.files
    ruta = str(archivo.path)
    verificar_golden(CASO / "esperado" / ruta, archivo.to_bytes())
    assert archivo.to_bytes() == (CASO / "original" / ruta).read_bytes()
