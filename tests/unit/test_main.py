from recetas.main import build_registry


def test_el_modulo_pospago_queda_registrado() -> None:
    registry = build_registry()

    assert "creacion_planes_pospago" in registry
    assert registry.modules()[0].info.name == "Creación de planes Pospago"
