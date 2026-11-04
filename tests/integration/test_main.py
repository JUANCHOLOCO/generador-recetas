from pathlib import Path

import pytest

from recetas.config import AppPaths
from recetas.main import build_context, build_registry

pytestmark = pytest.mark.integration


def test_build_context_crea_y_migra_la_base(tmp_path: Path) -> None:
    build_context(AppPaths(base=tmp_path))

    assert (tmp_path / "recetas.db").is_file()


def test_los_modulos_quedan_registrados_en_orden(tmp_path: Path) -> None:
    registry = build_registry(build_context(AppPaths(base=tmp_path)))

    assert [m.info.name for m in registry.modules()] == [
        "Creación de planes Pospago",
        "Alza de tarifas",
    ]
