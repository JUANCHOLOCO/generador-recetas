import sys
from pathlib import Path

import pytest

from recetas.config import AppPaths


def test_rutas_se_derivan_de_la_base(tmp_path: Path) -> None:
    paths = AppPaths(base=tmp_path)

    assert paths.database == tmp_path / "recetas.db"
    assert paths.output == tmp_path / "output"
    assert paths.backups == tmp_path / "backups"
    assert paths.logs == tmp_path / "logs"


def test_en_desarrollo_la_base_es_la_raiz_del_repositorio() -> None:
    assert (AppPaths.default().base / "pyproject.toml").is_file()


def test_en_ejecutable_portable_la_base_es_la_carpeta_del_exe(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(tmp_path / "GeneradorRecetas.exe"))

    assert AppPaths.default().base == tmp_path


def test_app_paths_es_inmutable(tmp_path: Path) -> None:
    paths = AppPaths(base=tmp_path)

    with pytest.raises(AttributeError):
        paths.base = Path("otra")  # type: ignore[misc]
