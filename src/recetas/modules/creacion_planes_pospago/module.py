"""Registro del módulo Creación de planes Pospago."""

from PySide6.QtWidgets import QTabWidget, QWidget

from recetas import __version__
from recetas.core.infrastructure.files.escritor import EscritorDeRecetas
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.core.plugins import AppContext, Module, ModuleInfo
from recetas.modules.creacion_planes_pospago.application.generar_receta import GenerarReceta
from recetas.modules.creacion_planes_pospago.infrastructure.repositories import (
    SqlParametrizacionRepository,
)
from recetas.modules.creacion_planes_pospago.infrastructure.seeds import (
    cargar_parametrizacion_inicial,
)
from recetas.modules.creacion_planes_pospago.ui.formulario_presenter import FormularioPresenter
from recetas.modules.creacion_planes_pospago.ui.formulario_view import FormularioView

INFO = ModuleInfo(
    id="creacion_planes_pospago",
    name="Creación de planes Pospago",
    description="Genera los instaladores SQL para nuevos planes Pospago (Corriente o Anticipada).",
    order=10,
)


class CreacionPlanesPospagoModule(Module):
    def __init__(self, context: AppContext) -> None:
        self._context = context

    @property
    def info(self) -> ModuleInfo:
        return INFO

    def initialize(self) -> None:
        cargar_parametrizacion_inicial(self._context.session_factory)

    def create_widget(self, parent: QWidget | None = None) -> QWidget:
        vista = FormularioView(
            autor_sugerido=self._context.usuario.nombre(),
            carpeta_sugerida=str(self._context.paths.output),
        )
        presenter = FormularioPresenter(
            vista,
            self.generar_receta(),
            EscritorDeRecetas(),
            SqlParametrizacionRepository(self._context.session_factory),
        )
        vista.generar_solicitado.connect(lambda: presenter.generar(vista.datos()))

        pestanas = QTabWidget(parent)
        pestanas.addTab(vista, "Generar receta")
        return pestanas

    def generar_receta(self) -> GenerarReceta:
        """Caso de uso con sus dependencias reales."""
        return GenerarReceta(
            SqlParametrizacionRepository(self._context.session_factory),
            JinjaRenderer("recetas.modules.creacion_planes_pospago", "recetas.core"),
            self._context.reloj,
            __version__,
        )
