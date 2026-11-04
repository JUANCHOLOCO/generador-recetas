"""Registro del módulo Alza de tarifas."""

from pathlib import Path

from PySide6.QtWidgets import QTabWidget, QWidget

from recetas import __version__
from recetas.core.infrastructure.files.escritor import EscritorDeRecetas
from recetas.core.infrastructure.files.excel import LectorExcel
from recetas.core.infrastructure.templating.jinja import JinjaRenderer
from recetas.core.plugins import AppContext, Module, ModuleInfo
from recetas.modules.alza_tarifas.application.generar_alza import GenerarAlzaPlanes
from recetas.modules.alza_tarifas.ui.formulario_presenter import (
    CLAVE_AUTOR,
    CLAVE_CARPETA,
    FormularioAlzaPresenter,
)
from recetas.modules.alza_tarifas.ui.formulario_view import FormularioAlzaView
from recetas.modules.alza_tarifas.ui.tipos_formulario import PLANES

INFO = ModuleInfo(
    id="alza_tarifas",
    name="Alza de tarifas",
    description="Genera los scripts de alza de tarifas (aplica y rollback) en ACTIVATOR.",
    order=20,
)


class AlzaTarifasModule(Module):
    def __init__(self, context: AppContext) -> None:
        self._context = context

    @property
    def info(self) -> ModuleInfo:
        return INFO

    def create_widget(self, parent: QWidget | None = None) -> QWidget:
        preferencias = self._context.preferencias
        vista = FormularioAlzaView(
            PLANES,
            autor_sugerido=preferencias.leer(CLAVE_AUTOR) or self._context.usuario.nombre(),
            carpeta_sugerida=preferencias.leer(CLAVE_CARPETA) or str(self._context.paths.output),
        )
        presenter = FormularioAlzaPresenter(
            PLANES, vista, self.generar_alza(), EscritorDeRecetas(), LectorExcel(), preferencias
        )
        vista.generar_solicitado.connect(lambda: presenter.generar(vista.datos()))
        vista.importar_solicitado.connect(
            lambda ruta: presenter.importar(Path(ruta), vista.datos().filas)
        )
        vista.limpiar_solicitado.connect(lambda: presenter.limpiar(vista.datos()))

        pestanas = QTabWidget(parent)
        pestanas.addTab(vista, "Planes pospago")  # la Fase 8B agrega "Paquetes"
        return pestanas

    def generar_alza(self) -> GenerarAlzaPlanes:
        """Caso de uso con sus dependencias reales."""
        return GenerarAlzaPlanes(
            JinjaRenderer("recetas.modules.alza_tarifas", "recetas.core"),
            self._context.reloj,
            __version__,
        )
