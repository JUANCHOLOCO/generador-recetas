import pytest
from pydantic import TypeAdapter, ValidationError

from recetas.modules.alza_tarifas.domain.valores import Precio, sql_numero

PRECIO: TypeAdapter[Precio] = TypeAdapter(Precio)


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("68083", "68083"),
        ("10605,04", "10605.04"),
        ("10605.04", "10605.04"),
        (" 51246,3 ", "51246.3"),
        ("89256,90", "89256.90"),
        ("0", "0"),
    ],
)
def test_precio_acepta_coma_o_punto_y_se_escribe_con_punto(texto: str, esperado: str) -> None:
    assert sql_numero(PRECIO.validate_python(texto)) == esperado


@pytest.mark.parametrize("texto", ["", "-100", "10.555", "1.234,56", "abc", "68 083"])
def test_precio_invalido(texto: str) -> None:
    with pytest.raises(ValidationError):
        PRECIO.validate_python(texto)
