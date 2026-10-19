from pathlib import PurePosixPath

import pytest

from recetas.core.domain.errors import (
    DuplicateRecipeFileError,
    InvalidRecipeContentError,
    InvalidRecipePathError,
)
from recetas.core.domain.recipe_bundle import RecipeBundle


def test_agrega_archivos_encadenando_llamadas() -> None:
    bundle = (
        RecipeBundle("TPFB-2753")
        .add("Corriente/Script/ACTIVADOR/aplica-cambio.sql", "EXIT")
        .add("Corriente/Conf/Pool-RQ-TPFB-2753_CORRIENTE.txt", "Plan 1")
    )

    assert len(bundle) == 2
    assert "Corriente/Script/ACTIVADOR/aplica-cambio.sql" in bundle
    assert bundle.root == PurePosixPath("TPFB-2753")


def test_files_se_entregan_ordenados_por_ruta() -> None:
    bundle = RecipeBundle("RQ").add("b/2.sql", "").add("a/1.sql", "").add("b/1.sql", "")

    assert [str(f.path) for f in bundle.files] == ["a/1.sql", "b/1.sql", "b/2.sql"]


def test_archivo_duplicado_falla() -> None:
    bundle = RecipeBundle("RQ").add("a.sql", "x")

    with pytest.raises(DuplicateRecipeFileError):
        bundle.add("a.sql", "y")


@pytest.mark.parametrize(
    "ruta_invalida",
    ["", "/absoluta.sql", "C:/receta/a.sql", "carpeta\\a.sql", "../fuera.sql", "a/../../b.sql"],
)
def test_rutas_invalidas_fallan(ruta_invalida: str) -> None:
    with pytest.raises(InvalidRecipePathError):
        RecipeBundle("RQ").add(ruta_invalida, "x")


def test_raiz_invalida_falla() -> None:
    with pytest.raises(InvalidRecipePathError):
        RecipeBundle("../RQ")


def test_por_defecto_codifica_en_cp1252_con_crlf() -> None:
    bundle = RecipeBundle("RQ").add("a.sql", "-- Creación\nEXIT\n")

    assert bundle.get("a.sql").to_bytes() == b"-- Creaci\xf3n\r\nEXIT\r\n"


def test_no_duplica_retornos_si_el_texto_ya_trae_crlf() -> None:
    bundle = RecipeBundle("RQ").add("a.sql", "uno\r\ndos\n")

    assert bundle.get("a.sql").to_bytes() == b"uno\r\ndos\r\n"


def test_permite_otra_codificacion_y_fin_de_linea() -> None:
    bundle = RecipeBundle("RQ").add("a.txt", "ñ\n", encoding="utf-8", newline="\n")

    assert bundle.get("a.txt").to_bytes() == "ñ\n".encode()


def test_caracter_fuera_de_cp1252_falla_al_agregar() -> None:
    with pytest.raises(InvalidRecipeContentError, match="✓"):
        RecipeBundle("RQ").add("a.sql", "Plan ✓ aprobado")
