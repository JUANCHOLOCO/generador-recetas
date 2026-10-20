"""Punto de entrada y composition root de la aplicación."""

import sys

from PySide6.QtWidgets import QApplication

from recetas.config import AppPaths
from recetas.core.infrastructure.db.migrator import upgrade_database
from recetas.core.plugins import ModuleRegistry
from recetas.modules import installed_modules
from recetas.ui.main_window import MainWindow


def build_registry() -> ModuleRegistry:
    registry = ModuleRegistry()
    for module in installed_modules():
        registry.register(module)
    return registry


def main() -> int:
    paths = AppPaths.default()
    upgrade_database(paths.database)

    app = QApplication(sys.argv)
    window = MainWindow(build_registry())
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
