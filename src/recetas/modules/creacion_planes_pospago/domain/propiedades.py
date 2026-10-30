"""Archivos .properties con los planes nuevos (docs/modulos/creacion_planes_pospago.md §5.5)."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum

from recetas.modules.creacion_planes_pospago.domain.estrategias import BillingStrategy
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Plan53
from recetas.modules.creacion_planes_pospago.domain.plan import PlanNuevo

# Consulta de Siebel para los planes 5.3, copiada literal de la macro (crearSiebelServiceProperties).
_CONSULTA_53 = (
    " as is5_3 from SIEBEL.S_ASSET a,  siebel.s_asset_x x, siebel.s_asset AP"
    " WHERE A.row_id  = x.row_id AND x.attrib_40 = ? AND A.status_cd = 'Activo'"
    " AND AP.status_cd = 'Activo' AND AP.type_cd = 'TELEFONIA_POS'"
    " AND AP.root_asset_id = A.row_id AND AP.prod_id in (SELECT  p.row_id"
    " FROM siebel.s_prod_int P, siebel.s_xa_class c WHERE  P.xa_class_id =  C.row_id"
    " AND C.NAME = 'Clase Tigo Pospago 5 0')"
)


class Ubicacion(StrEnum):
    """Carpeta del servidor donde vive el archivo, con la variable que usa el MOP."""

    JBOSS = "%JBOSS4_PROP%"
    WEBLOGIC = "%WEBLOGIC_PROP%"
    USSD = "%USSD_PROP%"


@dataclass(frozen=True, slots=True)
class ArchivoPropiedades:
    nombre: str
    ubicacion: Ubicacion
    lineas: tuple[str, ...]

    @property
    def contenido(self) -> str:
        return "".join(f"{linea}\n" for linea in self.lineas)


def lista(valores: Iterable[str]) -> str:
    """Valores separados por coma, con coma inicial: se agregan a la lista del servidor."""
    return "".join(f",{valor}" for valor in valores)


def linea_planes_53(planes: Sequence[PlanNuevo], planes_53: Sequence[Plan53]) -> str | None:
    """Línea SQL.ADD.ON.IS.NINTENDO de SiebelService, o None si ningún plan nuevo es 5.3."""
    nuevos = [p for p in planes if p.es_53]
    if not nuevos:
        return None
    registrados = {p.id_plan for p in planes_53}
    part_nums = [p.part_num for p in planes_53]
    part_nums += [p.part_num for p in nuevos if p.id_plan not in registrados]
    casos = "".join(f"'{part_num}','1'," for part_num in part_nums)
    return f"SQL.ADD.ON.IS.NINTENDO = select decode(AP.sp_num,{casos}'0'){_CONSULTA_53}"


def calcular_propiedades(
    planes: Sequence[PlanNuevo], planes_53: Sequence[Plan53], estrategia: BillingStrategy
) -> tuple[ArchivoPropiedades, ...]:
    """Los 6 archivos en el orden del MOP. `s` es el sufijo de las claves propias del tipo."""
    s = estrategia.sufijo_propiedades
    ids = lista(p.id_plan for p in planes)
    siebel = (linea_planes_53(planes, planes_53), f"idPlansNintendo{s}={ids}")
    return (
        ArchivoPropiedades(
            "InfranetService.properties", Ubicacion.JBOSS, (f"idPlansNintendo{s}={ids}",)
        ),
        ArchivoPropiedades(
            "PCRFService.properties",
            Ubicacion.JBOSS,
            (
                f"planCodeNintendo{s}={lista(p.codigo_pcrf for p in planes)}",
                f"idPlansNintendo{s}={lista(p.datos.svall for p in planes)}",
                f"idPlanNintendo{s}={ids}",
            ),
        ),
        ArchivoPropiedades(
            "PostSale.properties",
            Ubicacion.JBOSS,
            (
                f"PARAM_DESCRIPTION_NINTENDO={lista(p.nombre for p in planes)}",
                f"PARAM_ID_NINTENDO={ids}",
            ),
        ),
        ArchivoPropiedades("promotions.properties", Ubicacion.WEBLOGIC, (f"PLANSPOSPAGO5={ids}",)),
        ArchivoPropiedades(
            "SiebelService.properties", Ubicacion.JBOSS, tuple(linea for linea in siebel if linea)
        ),
        ArchivoPropiedades(
            "ussdGw.properties", Ubicacion.USSD, (f"Activator.idPlansNintendo{s}={ids}",)
        ),
    )