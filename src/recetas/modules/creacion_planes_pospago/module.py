"""Registro del módulo Creación de planes Pospago."""

from PySide6.QtWidgets import QTabWidget, QWidget

from recetas import __version__
from recetas.core.infrastructure.files.escritor import EscritorDeRecetas
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.core.plugins import AppContext, Module, ModuleInfo
from recetas.modules.creacion_planes_pospago.application.generar_receta import GenerarReceta
from recetas.modules.creacion_planes_pospago.infrastructure.mantenimiento import (
    tablas_de_parametrizacion,
)
from recetas.modules.creacion_planes_pospago.infrastructure.repositories import (
    SqlParametrizacionRepository,
)
from recetas.modules.creacion_planes_pospago.infrastructure.seeds import (
    cargar_parametrizacion_inicial,
)
from recetas.modules.creacion_planes_pospago.ui.formulario_presenter import FormularioPresenter
from recetas.modules.creacion_planes_pospago.ui.formulario_view import FormularioView
from recetas.ui.parametrizacion.presenter import ParametrizacionPresenter
from recetas.ui.parametrizacion.vista import ParametrizacionView

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
        # Pestaña 1: formulario de generación (Fase 6A)
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

        # Pestaña 2: mantenimiento de la parametrización (Fase 6B)
        tablas = tablas_de_parametrizacion(self._context.session_factory)
        mantenimiento = ParametrizacionView([t.titulo for t in tablas])
        parametros = ParametrizacionPresenter(mantenimiento, tablas)
        mantenimiento.tabla_elegida.connect(lambda indice: parametros.abrir(indice))
        mantenimiento.filtro_cambiado.connect(lambda tipo: parametros.filtrar(tipo))
        mantenimiento.guardar_solicitado.connect(lambda: parametros.guardar())
        mantenimiento.recargar_solicitado.connect(lambda: parametros.recargar())
        parametros.recargar()

        pestanas = QTabWidget(parent)
        pestanas.addTab(vista, "Generar receta")
        pestanas.addTab(mantenimiento, "Parametrización")
        return pestanas

    def generar_receta(self) -> GenerarReceta:
        """Caso de uso con sus dependencias reales."""
        return GenerarReceta(
            SqlParametrizacionRepository(self._context.session_factory),
            JinjaRenderer("recetas.modules.creacion_planes_pospago", "recetas.core"),
            self._context.reloj,
            __version__,
        )