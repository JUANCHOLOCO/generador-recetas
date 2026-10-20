from pathlib import Path

import pytest

from recetas.core.domain.billing import BillingScope
from recetas.core.infrastructure.db.seeding import leer_csv
from recetas.modules.creacion_planes_pospago.infrastructure.models import CanalModel


def test_convierte_cada_valor_segun_el_tipo_de_columna(tmp_path: Path) -> None:
    archivo = tmp_path / "canal.csv"
    archivo.write_text(
        "orden,nombre,tipo_facturacion,activo\n3,Retail,CORRIENTE,0\n", encoding="utf-8"
    )

    [canal] = list(leer_csv(archivo, CanalModel))

    assert canal.orden == 3
    assert canal.nombre == "Retail"
    assert canal.tipo_facturacion is BillingScope.CORRIENTE
    assert canal.activo is False


def test_columna_desconocida_falla_con_mensaje_claro(tmp_path: Path) -> None:
    archivo = tmp_path / "canal.csv"
    archivo.write_text("orden,nmbre\n1,Retail\n", encoding="utf-8")

    with pytest.raises(ValueError, match="nmbre"):
        list(leer_csv(archivo, CanalModel))
