import pytest
from jinja2 import UndefinedError

from recetas.core.domain.sql import es_literal_sql, sql_literal
from recetas.core.infrastructure.templating.jinja import JinjaRenderer


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        ("Pospago 5.1", "'Pospago 5.1'"),
        ("Plan D'Angelo", "'Plan D''Angelo'"),
        ("", "''"),
        (19900, "'19900'"),
        (None, "NULL"),
    ],
)
def test_sql_literal_escapa_comillas(valor: object, esperado: str) -> None:
    assert sql_literal(valor) == esperado


def test_variable_inexistente_falla() -> None:
    renderer = JinjaRenderer("recetas.core")

    with pytest.raises(UndefinedError):
        renderer.render("wrapper.sql.j2", esquema="ACTIVATOR")  # falta cab y script


@pytest.mark.parametrize("valor", ["null", "NULL", "63", "-9999", "'12055'", "'D''Angelo'", "''"])
def test_literales_sql_validos(valor: str) -> None:
    assert es_literal_sql(valor)


@pytest.mark.parametrize("valor", ["1; DROP TABLE X", "'abc", "'a' || 'b'", "CONTROL", "'a'b'"])
def test_literales_sql_invalidos(valor: str) -> None:
    assert not es_literal_sql(valor)
