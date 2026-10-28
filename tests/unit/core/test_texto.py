import pytest

from recetas.core.domain.texto import tiene_caracteres_de_control


@pytest.mark.parametrize("texto", ["Plan\n5.1", "Plan\t5.1", "Plan\r\n/", "a\x00b"])
def test_detecta_caracteres_de_control(texto: str) -> None:
    assert tiene_caracteres_de_control(texto)


@pytest.mark.parametrize("texto", ["Pospago Conectados 5.1 FC", "Creación ñ", "D'Angelo", ""])
def test_texto_normal_no_tiene_caracteres_de_control(texto: str) -> None:
    assert not tiene_caracteres_de_control(texto)