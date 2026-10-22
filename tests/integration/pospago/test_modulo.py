from pathlib import Path

import pytest

from recetas.config import AppPaths
from recetas.main import build_context
from recetas.modules.creacion_planes_pospago.module import CreacionPlanesPospagoModule
from tests.factories import crear_solicitud

pytestmark = pytest.mark.integration


def test_el_modulo_genera_una_receta_con_dependencias_reales(tmp_path: Path) -> None:
    modulo = CreacionPlanesPospagoModule(build_context(AppPaths(base=tmp_path)))
    modulo.initialize()

    receta = modulo.generar_receta().ejecutar(crear_solicitud())

    assert str(receta.bundle.root) == "TPFB-2753_Prod"
    assert len(receta.bundle) == 13