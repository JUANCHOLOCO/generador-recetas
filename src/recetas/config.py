"""Rutas de la aplicación, válidas en desarrollo y en el ejecutable portable."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


def _base_dir() -> Path:
    """Carpeta raíz donde viven la BD, la salida y los respaldos.

    - En el ejecutable portable (PyInstaller): la carpeta del .exe.
    - En desarrollo: la raíz del repositorio.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class AppPaths:
    base: Path

    @property
    def database(self) -> Path:
        return self.base / "recetas.db"

    @property
    def output(self) -> Path:
        return self.base / "output"

    @property
    def backups(self) -> Path:
        return self.base / "backups"

    @classmethod
    def default(cls) -> AppPaths:
        return cls(base=_base_dir())
