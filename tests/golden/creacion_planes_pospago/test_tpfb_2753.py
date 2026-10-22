"""Golden tests de TPFB-2753: salida estandarizada y equivalencia con los scripts originales."""

import re
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
from recetas.modules.creacion_planes_pospago.generators.promotions import PromotionsGenerator
from recetas.modules.creacion_planes_pospago.generators.siebel import SiebelGenerator
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


# ---------- Correcciones intencionales (docs/estandar-scripts.md, §7 y §8) ----------


def s_prod_int_x_con_alias(lista: list[str]) -> list[str]:
    """#8: Corriente escribe el INSERT a S_PROD_INT_X sin alias; es la misma sentencia."""
    return corregir(
        lista,
        [
            reemplazar(
                ")SELECT ROW_ID,CREATED_BY,LAST_UPD_BY,ROW_ID FROM SIEBEL.S_PROD_INT WHERE NAME=",
                ")SELECT SPI.ROW_ID,SPI.CREATED_BY,SPI.LAST_UPD_BY,SPI.ROW_ID"
                " FROM SIEBEL.S_PROD_INT SPI WHERE SPI.NAME=",
            ),
            reemplazar(
                "FROM SIEBEL.S_PROD_INT_X X WHERE X.ROW_ID=SIEBEL.S_PROD_INT.ROW_ID",
                "FROM SIEBEL.S_PROD_INT_X SPX WHERE SPX.ROW_ID=SPI.ROW_ID",
            ),
        ],
    )


_POID_PLAN_SIEBEL = re.compile(
    r"/PRODUCT \d+ 1'(,ATTRIB_44='0\.0\.0\.1 /SERVICE/CUENTACONTROL/TELEPHONY',"
    r"ATTRIB_45='0\.0\.0\.1 /DEAL (\d+) 0')"
)


def poid_plan_igual_al_deal(lista: list[str]) -> list[str]:
    """#6: en Corriente el /product del plan iba desfasado en 1 respecto del tarif group."""
    return [_POID_PLAN_SIEBEL.sub(r"/PRODUCT \2 1'\1", s) for s in lista]


_SINCRONIZACION_POID = re.compile(
    r"UPDATE PROMOTIONS\.TBL_PROM_POID_IDENTIFY SET POID='(\d+)' WHERE NAME_PACKAGE='(.+)'"
)


def poids_reales(lista: list[str]) -> list[str]:
    """C: el POID real va en el INSERT y desaparecen los UPDATE de sincronización."""
    poids: dict[str, str] = {}
    resto = []
    for s in lista:
        if m := _SINCRONIZACION_POID.fullmatch(s):
            poids[m.group(2)] = m.group(1)
        else:
            resto.append(s)
    return [
        re.sub(r",'([^']+)','99999',", lambda m: f",'{m.group(1)}','{poids[m.group(1)]}',", s)
        for s in resto
    ]


plan_type_solo_si_no_existe = reemplazar(  # B
    "VALUES(LAST_ID_TABLE,VARIABLE_TYPE,PLAN_NAME,PLAN_NAME,PLAN_NAME,CANCELABLE_PLAN)",
    "SELECT LAST_ID_TABLE,VARIABLE_TYPE,PLAN_NAME,PLAN_NAME,PLAN_NAME,CANCELABLE_PLAN FROM DUAL"
    " WHERE NOT EXISTS(SELECT 1 FROM PROMOTIONS.TBL_PROM_VARIABLES"
    " WHERE VARIABLE_TYPE='PLAN_TYPE' AND NAME='POSPAGO5')",
)

CORRECCIONES: dict[tuple[type[BaseSqlGenerator], str], list[Correccion]] = {
    (ActivadorGenerator, "SQL"): [],
    (ActivadorGenerator, "ROLLBACK"): [
        reemplazar("FROM SCORING_PLAN WHERE", "FROM ACTIVATOR.SCORING_PLAN WHERE"),  # #7
        reemplazar("FROM SERVICES S WHERE", "FROM ACTIVATOR.SERVICES S WHERE"),  # #7
    ],
    (SiebelGenerator, "SQL"): [s_prod_int_x_con_alias, poid_plan_igual_al_deal],
    (SiebelGenerator, "ROLLBACK"): [
        reemplazar("UPDATE CX_ADD_ONS_CATEGORY", "UPDATE SIEBEL.CX_ADD_ONS_CATEGORY"),  # #7
    ],
    (PromotionsGenerator, "SQL"): [poids_reales, plan_type_solo_si_no_existe],
    (PromotionsGenerator, "ROLLBACK"): [],
}


def _contenido(
    generador: BaseSqlGenerator, ctx: ContextoGeneracion, carpeta: str
) -> tuple[str, str]:
    if carpeta == "SQL":
        cab = generador.cabecera(ctx, generador.objetivo_aplica)
        return generador.nombre_script(ctx.rq), generador.contenido_script(ctx, cab)
    cab = generador.cabecera(ctx, generador.objetivo_rollback)
    return generador.nombre_rollback(ctx.rq), generador.contenido_rollback(ctx, cab)


@pytest.mark.parametrize("tipo", TIPOS)
@pytest.mark.parametrize("clase", GENERADORES)
@pytest.mark.parametrize("carpeta", ["SQL", "ROLLBACK"])
def test_scripts_de_datos(
    contextos_tpfb_2753: dict[BillingType, ContextoGeneracion],
    tipo: BillingType,
    clase: type[BaseSqlGenerator],
    carpeta: str,
) -> None:
    ctx = contextos_tpfb_2753[tipo]
    generador = clase(RENDERER)
    nombre, texto = _contenido(generador, ctx, carpeta)
    ruta = f"{ctx.estrategia.carpeta}/Script/{generador.carpeta}/{carpeta}/{nombre}"

    verificar_golden(CASO / "esperado" / ruta, a_bytes(ruta, texto))
    original = sentencias_sql(leer_original(CASO / "original" / ruta))
    verificar_equivalencia(
        sentencias_sql(texto), corregir(original, CORRECCIONES[(clase, carpeta)])
    )
