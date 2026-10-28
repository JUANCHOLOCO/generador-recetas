import pytest

from recetas.modules.creacion_planes_pospago.domain.errors import ParametrizacionIncompletaError
from recetas.modules.creacion_planes_pospago.generators.activador import valores_fila


def test_valor_estatico_que_no_es_literal_detiene_la_generacion() -> None:
    with pytest.raises(ParametrizacionIncompletaError, match="STATUS = '1; DROP TABLE X'"):
        valores_fila("PLANS", ("ID", "STATUS"), {"ID": "'7751'"}, {"STATUS": "1; DROP TABLE X"})


def test_valores_dinamicos_y_estaticos_validos() -> None:
    assert valores_fila("PLANS", ("ID", "STATUS"), {"ID": "'7751'"}, {"STATUS": "'1'"}) == (
        "'7751'",
        "'1'",
    )
