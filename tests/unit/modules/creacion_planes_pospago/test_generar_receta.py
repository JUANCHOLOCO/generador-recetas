from datetime import date

import pytest

from recetas.core.domain.billing import BillingType
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.modules.creacion_planes_pospago.application.generar_receta import GenerarReceta
from recetas.modules.creacion_planes_pospago.domain.errors import ParametrizacionIncompletaError
from tests.factories import crear_parametrizacion, crear_solicitud
from tests.fakes import ParametrizacionEnMemoria, RelojFijo

RENDERER = JinjaRenderer("recetas.modules.creacion_planes_pospago", "recetas.core")


def test_parametrizacion_incompleta_detiene_la_generacion() -> None:
    caso_de_uso = GenerarReceta(
        ParametrizacionEnMemoria({BillingType.CORRIENTE: crear_parametrizacion()}),
        RENDERER,
        RelojFijo(date(2026, 10, 22)),
        "0.1.0",
    )

    with pytest.raises(ParametrizacionIncompletaError, match="PLANS"):
        caso_de_uso.ejecutar(crear_solicitud())