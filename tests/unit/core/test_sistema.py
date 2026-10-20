import getpass
from datetime import date

import pytest

from recetas.core.infrastructure.sistema import RelojSistema, UsuarioSistemaOperativo


def test_reloj_del_sistema_devuelve_hoy() -> None:
    assert RelojSistema().hoy() == date.today()


def test_usuario_del_sistema_operativo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(getpass, "getuser", lambda: "jbotero")

    assert UsuarioSistemaOperativo().nombre() == "jbotero"


def test_usuario_desconocido_devuelve_texto_vacio(monkeypatch: pytest.MonkeyPatch) -> None:
    def sin_usuario() -> str:
        raise OSError("sin usuario")

    monkeypatch.setattr(getpass, "getuser", sin_usuario)

    assert UsuarioSistemaOperativo().nombre() == ""