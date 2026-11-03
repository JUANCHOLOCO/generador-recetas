from pathlib import Path

import pytest

from recetas.core.infrastructure.preferencias import PreferenciasJson

pytestmark = pytest.mark.integration


def test_guarda_y_lee_entre_instancias(tmp_path: Path) -> None:
    ruta = tmp_path / "preferencias.json"
    PreferenciasJson(ruta).guardar("autor", "José Peña")

    otra = PreferenciasJson(ruta)

    assert otra.leer("autor") == "José Peña"
    assert otra.leer("carpeta_salida") is None


def test_guardar_conserva_las_demas_claves(tmp_path: Path) -> None:
    preferencias = PreferenciasJson(tmp_path / "preferencias.json")
    preferencias.guardar("autor", "jbotero")
    preferencias.guardar("carpeta_salida", "D:/recetas")

    assert preferencias.leer("autor") == "jbotero"


def test_archivo_inexistente_o_danado_devuelve_none(tmp_path: Path) -> None:
    ruta = tmp_path / "preferencias.json"
    assert PreferenciasJson(ruta).leer("autor") is None

    ruta.write_text("{esto no es json", encoding="utf-8")
    assert PreferenciasJson(ruta).leer("autor") is None


def test_si_no_puede_guardar_no_lanza_error(tmp_path: Path) -> None:
    carpeta_inexistente = tmp_path / "no_existe" / "preferencias.json"

    PreferenciasJson(carpeta_inexistente).guardar("autor", "jbotero")  # no debe fallar

    assert PreferenciasJson(carpeta_inexistente).leer("autor") is None
