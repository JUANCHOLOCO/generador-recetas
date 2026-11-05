import pytest

from recetas.core.domain.texto import caracteres_fuera_de_cp1252, tiene_caracteres_de_control


@pytest.mark.parametrize("texto", ["Plan\n5.1", "Plan\t5.1", "Plan\r\n/", "a\x00b"])
def test_detecta_caracteres_de_control(texto: str) -> None:
    assert tiene_caracteres_de_control(texto)


@pytest.mark.parametrize("texto", ["Pospago Conectados 5.1 FC", "Creación ñ", "D'Angelo", ""])
def test_texto_normal_no_tiene_caracteres_de_control(texto: str) -> None:
    assert not tiene_caracteres_de_control(texto)


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("Plan 5.1 \u2192 FC", "'\u2192' (U+2192)"),
        ("Pospago\u200b5.1", "'\u200b' (U+200B)"),
        ("\U0001f600 Plan \U0001f600", "'\U0001f600' (U+1F600)"),
    ],
)
def test_detecta_caracteres_fuera_de_cp1252(texto: str, esperado: str) -> None:
    assert caracteres_fuera_de_cp1252(texto) == esperado


@pytest.mark.parametrize(
    "texto", ["Creación ñ", "\u201cPlan\u201d \u2013 5.1 \u20ac", "D'Angelo", ""]
)
def test_texto_que_cabe_en_cp1252(texto: str) -> None:
    assert caracteres_fuera_de_cp1252(texto) == ""
