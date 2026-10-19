import pytest

from recetas.core.domain.errors import DuplicateModuleError, UnknownModuleError
from recetas.core.plugins import ModuleRegistry
from tests.fakes import FakeModule


def test_registra_y_obtiene_un_modulo() -> None:
    registry = ModuleRegistry()
    modulo = FakeModule("alfa", "Alfa")

    registry.register(modulo)

    assert registry.get("alfa") is modulo
    assert "alfa" in registry
    assert len(registry) == 1


def test_registrar_dos_veces_el_mismo_id_falla() -> None:
    registry = ModuleRegistry()
    registry.register(FakeModule("alfa", "Alfa"))

    with pytest.raises(DuplicateModuleError):
        registry.register(FakeModule("alfa", "Otro nombre"))


def test_obtener_modulo_inexistente_falla() -> None:
    with pytest.raises(UnknownModuleError, match="beta"):
        ModuleRegistry().get("beta")


def test_lista_ordenada_por_orden_y_luego_por_nombre() -> None:
    registry = ModuleRegistry()
    registry.register(FakeModule("c", "Zeta", order=1))
    registry.register(FakeModule("b", "Beta", order=2))
    registry.register(FakeModule("a", "Alfa", order=2))

    nombres = [m.info.name for m in registry.modules()]

    assert nombres == ["Zeta", "Alfa", "Beta"]


def test_un_modulo_sin_implementar_el_contrato_no_se_puede_crear() -> None:
    from recetas.core.plugins import Module

    class ModuloIncompleto(Module):  # no implementa info ni create_widget
        pass

    with pytest.raises(TypeError):
        ModuloIncompleto()  # type: ignore[abstract]