"""Golden de punta a punta: JSON → caso de uso → disco, comparado con lo aprobado."""

from pathlib import Path

import pytest

from recetas.core.domain.billing import BillingType
from recetas.core.infrastructure.files.escritor import EscritorDeRecetas
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.creacion_planes_pospago.application.generar_receta import GenerarReceta
from recetas.modules.creacion_planes_pospago.domain.estrategias import estrategia_para
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta
from tests.fakes import ParametrizacionEnMemoria, RelojFijo
from tests.golden.conftest import CASO_TPFB_2753, FECHA, VERSION

pytestmark = pytest.mark.golden

RENDERER = JinjaRenderer("recetas.modules.creacion_planes_pospago", "recetas.core")


def _archivos(carpeta: Path, base: Path) -> dict[str, bytes]:
    return {
        p.relative_to(base).as_posix(): p.read_bytes() for p in carpeta.rglob("*") if p.is_file()
    }


@pytest.mark.parametrize("tipo", [BillingType.CORRIENTE, BillingType.ANTICIPADA])
def test_receta_completa_tpfb_2753(
    tmp_path: Path,
    tipo: BillingType,
    parametrizaciones_tpfb_2753: dict[BillingType, Parametrizacion],
    solicitudes_tpfb_2753: dict[BillingType, SolicitudReceta],
) -> None:
    caso_de_uso = GenerarReceta(
        ParametrizacionEnMemoria(parametrizaciones_tpfb_2753), RENDERER, RelojFijo(FECHA), VERSION
    )

    receta = caso_de_uso.ejecutar(solicitudes_tpfb_2753[tipo])
    raiz = EscritorDeRecetas().escribir(receta.bundle, tmp_path)

    carpeta = estrategia_para(tipo).carpeta
    esperado = CASO_TPFB_2753 / "esperado"
    generados = _archivos(raiz / carpeta, raiz)
    aprobados = _archivos(esperado / carpeta, esperado)

    assert raiz.name == "TPFB-2753_Prod"
    assert sorted(generados) == sorted(aprobados)
    for ruta, contenido in aprobados.items():
        assert generados[ruta] == contenido, f"{ruta} difiere del archivo aprobado"