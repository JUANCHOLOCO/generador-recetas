import logging
from pathlib import Path

import pytest

from recetas.core.infrastructure.bitacora import cerrar_bitacora, configurar_bitacora

pytestmark = pytest.mark.integration


def test_escribe_en_archivo_sin_duplicar_manejadores(tmp_path: Path) -> None:
    try:
        ruta = configurar_bitacora(tmp_path / "logs")
        configurar_bitacora(tmp_path / "logs")

        logging.getLogger("recetas.prueba").info("mensaje de prueba")

        assert len(logging.getLogger("recetas").handlers) == 1
    finally:
        cerrar_bitacora()
    assert "recetas.prueba: mensaje de prueba" in ruta.read_text(encoding="utf-8")