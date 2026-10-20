"""Punto de entrada y composition root de la aplicación."""

import sys

from PySide6.QtWidgets import QApplication

from recetas.config import AppPaths
from recetas.core.infrastructure.db.engine import create_session_factory, create_sqlite_engine
from recetas.core.infrastructure.db.migrator import upgrade_database
from recetas.core.plugins import AppContext, ModuleRegistry
from recetas.modules import installed_modules
from recetas.ui.main_window import MainWindow

def build_context(paths: AppPaths) -> AppContext:
    upgrade_database(paths.database)
    engine = create_sqlite_engine(paths.database)
    return AppContext(paths=paths, session_factory=create_session_factory(engine))

def build_registry(context: AppContext) -> ModuleRegistry:
    registry = ModuleRegistry()
    for module in installed_modules(context):
        registry.register(module)
    return registry

def main() -> int:
    context = build_context(AppPaths.default())
    registry = build_registry(context)
    for module in registry.modules():
        module.initialize()

    app = QApplication(sys.argv)
    window = MainWindow(registry)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())