from pathlib import Path

import pytest
from openpyxl import Workbook

from recetas.core.domain.errors import ImportacionError
from recetas.core.domain.importacion import FormatoHoja
from recetas.core.infrastructure.files.excel import LectorExcel

pytestmark = pytest.mark.integration

FORMATO = FormatoHoja(encabezados=("Id", "Valor"))


def test_lee_solo_la_primera_hoja(tmp_path: Path) -> None:
    libro = Workbook()
    hoja = libro.active
    hoja.append(["Id", "Valor"])
    hoja.append([775, 10605.04])
    libro.create_sheet("Otra").append(["no", "se lee"])
    ruta = tmp_path / "planes.xlsx"
    libro.save(ruta)

    assert LectorExcel().leer(ruta, FORMATO) == [["775", "10605.04"]]


def test_archivo_que_no_es_excel(tmp_path: Path) -> None:
    ruta = tmp_path / "planes.xlsx"
    ruta.write_text("no soy un excel", encoding="utf-8")

    with pytest.raises(ImportacionError, match="planes.xlsx"):
        LectorExcel().leer(ruta, FORMATO)
