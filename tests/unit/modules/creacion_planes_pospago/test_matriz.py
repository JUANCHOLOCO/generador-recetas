from recetas.modules.creacion_planes_pospago.domain.matriz import matriz_cambio_plan
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import IdCambioPlan
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan as L
from tests.factories import crear_parametrizacion

PARAMETRIZACION = crear_parametrizacion(
    ids_cambio_plan=(
        IdCambioPlan("1", L.PREPAGO),
        IdCambioPlan("7401", L.NINTENDO),
        IdCambioPlan("7411", L.NINTENDO),
        IdCambioPlan("7751", L.NINTENDO),  # plan del formulario ya registrado
        IdCambioPlan("1238", L.ATP),
        IdCambioPlan("C01", L.CONTROL),
    )
)
NUEVOS = ["7751", "7761"]


def _pares(id_plan: str) -> dict[L, tuple[tuple[str, str], ...]]:
    return {s.lista: s.pares for s in matriz_cambio_plan(id_plan, NUEVOS, PARAMETRIZACION)}


def test_secciones_en_el_orden_del_script() -> None:
    secciones = matriz_cambio_plan("7751", NUEVOS, PARAMETRIZACION)

    assert [s.lista for s in secciones] == [L.PREPAGO, L.NINTENDO, L.ATP, L.CONTROL]


def test_prepago_primero_el_plan_nuevo() -> None:
    assert _pares("7751")[L.PREPAGO] == (("7751", "1"), ("1", "7751"))


def test_nintendo_existentes_en_ambos_sentidos_y_otros_nuevos_en_uno() -> None:
    assert _pares("7751")[L.NINTENDO] == (
        ("7401", "7751"),
        ("7751", "7401"),
        ("7411", "7751"),
        ("7751", "7411"),
        ("7761", "7751"),
    )


def test_atp_y_control_en_un_solo_sentido_incluso_codigos() -> None:
    pares = _pares("7751")

    assert pares[L.ATP] == (("1238", "7751"),)
    assert pares[L.CONTROL] == (("C01", "7751"),)


def test_toda_la_receta_sin_pares_repetidos_ni_faltantes_entre_planes_nuevos() -> None:
    todos = [
        p for n in NUEVOS for s in matriz_cambio_plan(n, NUEVOS, PARAMETRIZACION) for p in s.pares
    ]

    assert len(todos) == len(set(todos))
    assert ("7751", "7761") in todos
    assert ("7761", "7751") in todos
    assert ("7751", "7751") not in todos
