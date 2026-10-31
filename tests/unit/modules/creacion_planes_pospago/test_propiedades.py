from recetas.core.domain.billing import BillingType
from recetas.modules.creacion_planes_pospago.domain.estrategias import estrategia_para
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Plan53
from recetas.modules.creacion_planes_pospago.domain.propiedades import (
    ArchivoPropiedades,
    Ubicacion,
    calcular_propiedades,
    linea_planes_53,
    lista,
)
from tests.factories import crear_plan

CORRIENTE = estrategia_para(BillingType.CORRIENTE)
ANTICIPADA = estrategia_para(BillingType.ANTICIPADA)


def _por_nombre(archivos: tuple[ArchivoPropiedades, ...]) -> dict[str, tuple[str, ...]]:
    return {a.nombre: a.lineas for a in archivos}


def test_lista_empieza_con_coma() -> None:
    assert lista(["775", "776"]) == ",775,776"


def test_corriente_usa_sufijo_salvo_en_postsale_y_promotions() -> None:
    archivos = _por_nombre(calcular_propiedades([crear_plan()], [], CORRIENTE))

    assert archivos == {
        "InfranetService.properties": ("idPlansNintendoCorriente=,7751",),
        "PCRFService.properties": (
            "planCodeNintendoCorriente=,Conectados_51_FC",
            "idPlansNintendoCorriente=,SVALL2632",
            "idPlanNintendoCorriente=,7751",
        ),
        "PostSale.properties": (
            "PARAM_DESCRIPTION_NINTENDO=,Pospago Conectados 5.1 FC",
            "PARAM_ID_NINTENDO=,7751",
        ),
        "promotions.properties": ("PLANSPOSPAGO5=,7751",),
        "SiebelService.properties": ("idPlansNintendoCorriente=,7751",),
        "ussdGw.properties": ("Activator.idPlansNintendoCorriente=,7751",),
    }


def test_anticipada_sin_sufijo() -> None:
    archivos = _por_nombre(calcular_propiedades([crear_plan(id_plan="775")], [], ANTICIPADA))

    assert archivos["InfranetService.properties"] == ("idPlansNintendo=,775",)
    assert archivos["ussdGw.properties"] == ("Activator.idPlansNintendo=,775",)


def test_sin_planes_5_3_no_hay_linea_de_siebel() -> None:
    assert linea_planes_53([crear_plan()], [Plan53("741", "PLCON0332")]) is None


def test_linea_5_3_lleva_los_olds_y_luego_los_nuevos_5_3() -> None:
    planes = [crear_plan(es_53=True), crear_plan(id_plan="7761", part_num="PLCON0455")]

    linea = linea_planes_53(planes, [Plan53("741", "PLCON0332")])

    assert linea is not None
    assert linea.startswith(
        "SQL.ADD.ON.IS.NINTENDO = select decode(AP.sp_num,"
        "'PLCON0332','1','PLCON0454','1','0') as is5_3 from SIEBEL.S_ASSET"
    )


def test_plan_5_3_ya_registrado_no_se_repite() -> None:
    linea = linea_planes_53([crear_plan(es_53=True)], [Plan53("7751", "PLCON0454")])

    assert linea is not None
    assert linea.count("PLCON0454") == 1


def test_siebel_lleva_la_linea_5_3_antes_de_los_ids() -> None:
    archivos = _por_nombre(calcular_propiedades([crear_plan(es_53=True)], [], CORRIENTE))

    linea_53, ids = archivos["SiebelService.properties"]
    assert linea_53.startswith("SQL.ADD.ON.IS.NINTENDO")
    assert ids == "idPlansNintendoCorriente=,7751"


def test_contenido_tiene_una_propiedad_por_linea() -> None:
    archivo = ArchivoPropiedades("x.properties", Ubicacion.JBOSS, ("a=,1", "b=,2"))

    assert archivo.contenido == "a=,1\nb=,2\n"
