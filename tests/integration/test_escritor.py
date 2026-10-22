from pathlib import Path

import pytest

from recetas.core.domain.errors import RecetaExistenteError
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.infrastructure.files.escritor import EscritorDeRecetas

pytestmark = pytest.mark.integration


def _bundle(carpeta: str, contenido: str = "EXIT\n") -> RecipeBundle:
    return (
        RecipeBundle("TPFB-2753_Prod")
        .add(f"{carpeta}/Script/ACTIVADOR/aplica-cambio.sql", contenido)
        .add(f"{carpeta}/Conf/Pool.txt", "Plan\n")
    )


def test_escribe_cada_archivo_con_sus_bytes(tmp_path: Path) -> None:
    raiz = EscritorDeRecetas().escribir(_bundle("Corriente", "Creación\n"), tmp_path)

    assert raiz == tmp_path / "TPFB-2753_Prod"
    assert (raiz / "Corriente/Script/ACTIVADOR/aplica-cambio.sql").read_bytes() == b"Creaci\xf3n\r\n"
    assert (raiz / "Corriente/Conf/Pool.txt").is_file()


def test_no_sobrescribe_sin_confirmacion(tmp_path: Path) -> None:
    escritor = EscritorDeRecetas()
    escritor.escribir(_bundle("Corriente"), tmp_path)

    with pytest.raises(RecetaExistenteError, match="Corriente"):
        escritor.escribir(_bundle("Corriente"), tmp_path)


def test_sobrescribir_reemplaza_la_seccion_completa(tmp_path: Path) -> None:
    escritor = EscritorDeRecetas()
    raiz = escritor.escribir(_bundle("Corriente"), tmp_path)
    sobrante = raiz / "Corriente/archivo_viejo.txt"
    sobrante.write_text("viejo")

    escritor.escribir(_bundle("Corriente", "NUEVO\n"), tmp_path, sobrescribir=True)

    assert not sobrante.exists()
    assert (raiz / "Corriente/Script/ACTIVADOR/aplica-cambio.sql").read_text() == "NUEVO\n"


def test_otro_tipo_de_facturacion_convive_en_la_misma_raiz(tmp_path: Path) -> None:
    escritor = EscritorDeRecetas()
    escritor.escribir(_bundle("Corriente"), tmp_path)

    raiz = escritor.escribir(_bundle("Anticipados"), tmp_path)

    assert sorted(p.name for p in raiz.iterdir()) == ["Anticipados", "Corriente"]


def test_no_deja_carpetas_temporales(tmp_path: Path) -> None:
    raiz = EscritorDeRecetas().escribir(_bundle("Corriente"), tmp_path)

    assert not [p for p in raiz.iterdir() if p.name.startswith(".tmp-")]


def test_receta_vacia_falla(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        EscritorDeRecetas().escribir(RecipeBundle("RQ"), tmp_path)