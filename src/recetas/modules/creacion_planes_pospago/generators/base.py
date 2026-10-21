"""Estructura común de los generadores de scripts (patrón Template Method)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from recetas.core.application.ports import TemplateRenderer
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.core.domain.scripts import CabeceraScript
from recetas.modules.creacion_planes_pospago.domain.estrategias import (
    BillingStrategy,
    estrategia_para,
)
from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta


@dataclass(frozen=True, slots=True)
class ContextoGeneracion:
    """Todo lo que un generador necesita para producir sus archivos."""

    solicitud: SolicitudReceta
    parametrizacion: Parametrizacion
    estrategia: BillingStrategy
    fecha: date
    version: str

    @classmethod
    def crear(
        cls,
        solicitud: SolicitudReceta,
        parametrizacion: Parametrizacion,
        fecha: date,
        version: str,
    ) -> ContextoGeneracion:
        if parametrizacion.tipo is not solicitud.tipo:
            raise ValueError("La parametrización y la solicitud son de tipos distintos.")
        return cls(solicitud, parametrizacion, estrategia_para(solicitud.tipo), fecha, version)

    @property
    def rq(self) -> str:
        """Requerimiento tal como va en nombres de archivo y cabeceras."""
        return self.estrategia.rq_archivos(self.solicitud.requerimiento)


class BaseSqlGenerator(ABC):
    """Genera los 4 archivos de una base de datos: 2 wrappers, script y rollback."""

    def __init__(self, renderer: TemplateRenderer) -> None:
        self._renderer = renderer

    # ---- Lo que cada base de datos define ----

    @property
    @abstractmethod
    def esquema(self) -> str:
        """Esquema Oracle (CURRENT_SCHEMA y 'BASE DE DATOS' en la cabecera)."""

    @property
    @abstractmethod
    def carpeta(self) -> str:
        """Carpeta dentro de Script/."""

    @property
    @abstractmethod
    def objetivo_aplica(self) -> str: ...

    @property
    @abstractmethod
    def objetivo_rollback(self) -> str: ...

    @abstractmethod
    def nombre_script(self, rq: str) -> str: ...

    @abstractmethod
    def nombre_rollback(self, rq: str) -> str: ...

    @abstractmethod
    def contenido_script(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str: ...

    @abstractmethod
    def contenido_rollback(self, ctx: ContextoGeneracion, cab: CabeceraScript) -> str: ...

    # ---- Lo que es igual para todas (Template Method) ----

    def generar(self, ctx: ContextoGeneracion, bundle: RecipeBundle) -> None:
        base = f"{ctx.estrategia.carpeta}/Script/{self.carpeta}"
        cab_aplica = self.cabecera(ctx, self.objetivo_aplica)
        cab_rollback = self.cabecera(ctx, self.objetivo_rollback)

        bundle.add(f"{base}/aplica-cambio.sql", self.wrapper_aplica(ctx))
        bundle.add(f"{base}/rollback-cambio.sql", self.wrapper_rollback(ctx))
        bundle.add(
            f"{base}/SQL/{self.nombre_script(ctx.rq)}", self.contenido_script(ctx, cab_aplica)
        )
        bundle.add(
            f"{base}/ROLLBACK/{self.nombre_rollback(ctx.rq)}",
            self.contenido_rollback(ctx, cab_rollback),
        )

    def cabecera(self, ctx: ContextoGeneracion, objetivo: str) -> CabeceraScript:
        return CabeceraScript(
            requerimiento=ctx.rq,
            objetivo=objetivo,
            base_datos=self.esquema,
            autor=ctx.solicitud.autor,
            fecha=ctx.fecha,
            version=ctx.version,
        )

    def wrapper_aplica(self, ctx: ContextoGeneracion) -> str:
        return self._wrapper(
            self.cabecera(ctx, self.objetivo_aplica), f"SQL/{self.nombre_script(ctx.rq)}"
        )

    def wrapper_rollback(self, ctx: ContextoGeneracion) -> str:
        return self._wrapper(
            self.cabecera(ctx, self.objetivo_rollback), f"ROLLBACK/{self.nombre_rollback(ctx.rq)}"
        )

    def _wrapper(self, cab: CabeceraScript, script: str) -> str:
        return self._renderer.render("wrapper.sql.j2", cab=cab, esquema=self.esquema, script=script)
