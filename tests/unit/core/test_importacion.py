import pytest

from recetas.core.domain.errors import ImportacionError
from recetas.core.domain.importacion import FormatoHoja, a_texto, extraer_filas, letra_columna

FORMATO = FormatoHoja(encabezados=("Id", "Nombre", "Valor"), fila_encabezado=2)


@pytest.mark.parametrize(
    ("valor", "texto"),
    [
        (None, ""),
        (775, "775"),
        (19900.0, "19900"),
        (10605.04, "10605.04"),
        ("  PLCON0446 ", "PLCON0446"),
    ],
)
def test_a_texto(valor: object, texto: str) -> None:
    assert a_texto(valor) == texto


@pytest.mark.parametrize(("indice", "letra"), [(0, "A"), (3, "D"), (25, "Z"), (26, "AA")])
def test_letra_columna(indice: int, letra: str) -> None:
    assert letra_columna(indice) == letra


def test_devuelve_las_filas_de_datos_sin_vacias_y_con_el_ancho_del_formato() -> None:
    celdas: list[tuple[object, ...]] = [
        ("Título de grupo", None, None),
        ("Id", "Nombre", "Valor"),
        (775, "Plan 5.1", 19900, "columna extra"),
        (None, None, None),
        (776, "Plan 5.2"),
    ]

    assert extraer_filas(celdas, FORMATO) == [
        ["775", "Plan 5.1", "19900"],
        ["776", "Plan 5.2", ""],
    ]


def test_compara_encabezados_sin_importar_mayusculas_ni_espacios() -> None:
    celdas: list[tuple[object, ...]] = [(), ("  ID ", "nombre", "VALOR")]

    assert extraer_filas(celdas, FORMATO) == []


def test_encabezado_distinto_indica_la_celda() -> None:
    celdas: list[tuple[object, ...]] = [(), ("Id", "Nombre", "Precio")]

    with pytest.raises(ImportacionError, match="celda C2 debe decir 'Valor' y dice 'Precio'"):
        extraer_filas(celdas, FORMATO)


def test_sin_fila_de_encabezados() -> None:
    with pytest.raises(ImportacionError, match="fila 2"):
        extraer_filas([("Id", "Nombre", "Valor")], FORMATO)