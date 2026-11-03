from datetime import date

from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.alza_tarifas.application.generar_alza import GenerarAlzaPlanes
from tests.factories import crear_solicitud_alza, datos_plan_alza
from tests.fakes import RelojFijo

RENDERER = JinjaRenderer("recetas.modules.alza_tarifas", "recetas.core")


def test_arma_la_receta_en_la_carpeta_del_ambiente_con_sus_advertencias() -> None:
    solicitud = crear_solicitud_alza(datos_plan_alza(precio_nuevo="60000"))

    alza = GenerarAlzaPlanes(RENDERER, RelojFijo(date(2026, 11, 3)), "0.1.0").ejecutar(solicitud)

    assert str(alza.bundle.root) == "TPFB-1726_Prod"
    assert len(alza.bundle) == 4
    assert [a.fila for a in alza.advertencias] == [1]
