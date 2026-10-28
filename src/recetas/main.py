"""Punto de entrada y composition root de la aplicación."""

import logging
import sys

from PySide6.QtWidgets import QApplication

from recetas import __version__
from recetas.config import AppPaths
from recetas.core.infrastructure.bitacora import configurar_bitacora
from recetas.core.infrastructure.db.engine import create_session_factory, create_sqlite_engine
from recetas.core.infrastructure.db.migrator import upgrade_database
from recetas.core.infrastructure.sistema import RelojSistema, UsuarioSistemaOperativo
from recetas.core.plugins import AppContext, ModuleRegistry
from recetas.modules import installed_modules
from recetas.ui.errores import instalar_manejador_global
from recetas.ui.main_window import MainWindow
from recetas.ui.tema import aplicar_tema

logger = logging.getLogger(__name__)

def build_context(paths: AppPaths) -> AppContext:
    upgrade_database(paths.database)
    engine = create_sqlite_engine(paths.database)
    return AppContext(
        paths=paths,
        session_factory=create_session_factory(engine),
        reloj=RelojSistema(),
        usuario=UsuarioSistemaOperativo(),
    )


def build_registry(context: AppContext) -> ModuleRegistry:
    registry = ModuleRegistry()
    for module in installed_modules(context):
        registry.register(module)
    return registry


def main() -> int:
    app = QApplication(sys.argv)
    aplicar_tema(app)
    paths = AppPaths.default()
    instalar_manejador_global(configurar_bitacora(paths.logs))
    logger.info("Inicio del Generador de Recetas %s", __version__)

    context = build_context(paths)
    registry = build_registry(context)
    for module in registry.modules():
        module.initialize()

    window = MainWindow(registry)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
