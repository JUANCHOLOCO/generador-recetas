import sys
from pathlib import Path

import pytest

from recetas.ui.errores import instalar_manejador_global


def test_error_no_controlado_se_registra_y_se_informa(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setattr(sys, "excepthook", sys.excepthook)  # se restaura al terminar
    mostrados: list[str] = []
    instalar_manejador_global(Path("C:/app/logs/recetas.log"), mostrados.append)

    sys.excepthook(ValueError, ValueError("dato raro"), None)

    assert "dato raro" in mostrados[0]
    assert "recetas.log" in mostrados[0]
    assert "Error no controlado" in caplog.text