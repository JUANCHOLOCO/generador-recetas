import pytest
from jinja2 import UndefinedError

from recetas.core.infrastructure.templating.jinja import JinjaRenderer, sql_literal


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