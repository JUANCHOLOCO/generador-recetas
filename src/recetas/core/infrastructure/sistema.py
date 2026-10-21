"""Adaptadores de los puertos Reloj y UsuarioActual sobre el sistema operativo."""

import getpass
from datetime import date


class RelojSistema:
    def hoy(self) -> date:
        return date.today()


class UsuarioSistemaOperativo:
    """Usuario de Windows. Se reemplazará por el usuario logueado cuando exista login."""

    def nombre(self) -> str:
        try:
            return getpass.getuser()
        except OSError:
            return ""
