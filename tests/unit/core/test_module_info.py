import pytest

from recetas.core.plugins import ModuleInfo


def test_crea_info_valida_con_valores_por_defecto() -> None:
    info = ModuleInfo(id="alza_tarifas", name="Alza de tarifas")

    assert info.description == ""
    assert info.order == 100


@pytest.mark.parametrize("id_invalido", ["", "Alza", "alza-tarifas", "1alza", "alza tarifas"])
def test_id_invalido_falla(id_invalido: str) -> None:
    with pytest.raises(ValueError, match="Id de módulo inválido"):
        ModuleInfo(id=id_invalido, name="X")


def test_nombre_vacio_falla() -> None:
    with pytest.raises(ValueError, match="nombre"):
        ModuleInfo(id="alza", name="   ")