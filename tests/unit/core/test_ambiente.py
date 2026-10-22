import pytest

from recetas.core.domain.ambiente import Ambiente


@pytest.mark.parametrize(
    ("ambiente", "sufijo"),
    [(Ambiente.DEV, "Dev"), (Ambiente.UAT, "UAT"), (Ambiente.PROD, "Prod")],
)
def test_sufijo_de_la_carpeta(ambiente: Ambiente, sufijo: str) -> None:
    assert ambiente.sufijo == sufijo