from pathlib import Path

import pytest

from recetas.core.infrastructure.files.excel import LectorExcel
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta
from recetas.modules.creacion_planes_pospago.ui.formulario_presenter import (
    FORMATO_EXCEL,
    DatosFormulario,
    construir_solicitud,
)

pytestmark = pytest.mark.integration

ENTRADA = Path(__file__).parents[2] / "golden" / "creacion_planes_pospago" / "TPFB-2753" / "entrada"


@pytest.mark.parametrize(
    ("archivo", "tipo", "primer_id"),
    [
        ("PlanesAnticipados.xlsx", "ANTICIPADA", "775"),
        ("PlanesCorrientes.xlsx", "CORRIENTE", "7751"),
    ],
)
def test_los_excel_reales_se_importan_y_pasan_la_validacion(
    archivo: str, tipo: str, primer_id: str
) -> None:
    filas = LectorExcel().leer(ENTRADA / archivo, FORMATO_EXCEL)
    datos = DatosFormulario(
        requerimiento="TPFB-2753",
        autor="Equipo Tecnico",
        ambiente="PROD",
        tipo=tipo,
        carpeta="C:/recetas",
        filas=filas,
    )

    solicitud = SolicitudReceta.model_validate(construir_solicitud(datos)[0])

    assert len(solicitud.planes) == 8
    assert solicitud.planes[0].id_plan == primer_id
