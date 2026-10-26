"""Lógica de la pantalla de mantenimiento de parametrización (MVP, sin Qt)."""

from collections.abc import Sequence
from typing import Protocol

from recetas.core.application.mantenimiento import (
    ColumnaEditable,
    ErrorCelda,
    FilaParametro,
    ParametrizacionInvalidaError,
    TablaMantenible,
)

_TIPO = "tipo_facturacion"
_AMBAS = "AMBAS"


class VistaParametrizacion(Protocol):
    def mostrar_tabla(
        self,
        columnas: Sequence[ColumnaEditable],
        filas: Sequence[list[str]],
        claves: Sequence[int | None],
    ) -> None: ...
    def filas(self) -> list[list[str]]: ...
    def claves(self) -> list[int | None]: ...
    def mostrar_solo(self, visibles: set[int] | None) -> None: ...
    def seleccionar_tabla(self, indice: int) -> None: ...
    def mostrar_errores(self, errores: Sequence[ErrorCelda]) -> None: ...
    def confirmar(self, titulo: str, texto: str) -> bool: ...
    def mostrar_resultado(self, mensaje: str) -> None: ...


class ParametrizacionPresenter:
    def __init__(self, vista: VistaParametrizacion, tablas: Sequence[TablaMantenible]) -> None:
        self._vista = vista
        self._tablas = list(tablas)
        self._actual = 0
        self._filtro = ""
        self._cargadas: list[list[str]] = []
        self._claves_cargadas: set[int] = set()

    def abrir(self, indice: int) -> None:
        if indice == self._actual:
            return
        if self._hay_cambios() and not self._vista.confirmar(
            "Cambios sin guardar", "La tabla actual tiene cambios sin guardar. ¿Descartarlos?"
        ):
            self._vista.seleccionar_tabla(self._actual)
            return
        self._actual = indice
        self.recargar()

    def recargar(self) -> None:
        tabla = self._tablas[self._actual]
        columnas = tabla.columnas()
        filas = tabla.listar()
        texto = [[f.valores.get(c.nombre, "") for c in columnas] for f in filas]
        self._cargadas = [fila.copy() for fila in texto]
        self._claves_cargadas = {f.id for f in filas if f.id is not None}
        self._vista.mostrar_tabla(columnas, texto, [f.id for f in filas])
        self._vista.mostrar_errores([])
        self.filtrar(self._filtro)

    def filtrar(self, tipo: str) -> None:
        """Oculta (no elimina) las filas que no aplican al tipo de facturación elegido."""
        self._filtro = tipo
        nombres = [c.nombre for c in self._tablas[self._actual].columnas()]
        if not tipo or _TIPO not in nombres:
            self._vista.mostrar_solo(None)
            return
        i = nombres.index(_TIPO)
        visibles = {n for n, fila in enumerate(self._vista.filas()) if fila[i] in (tipo, _AMBAS, "")}
        self._vista.mostrar_solo(visibles)

    def guardar(self) -> None:
        tabla = self._tablas[self._actual]
        nombres = [c.nombre for c in tabla.columnas()]
        filas = [
            FilaParametro(clave, dict(zip(nombres, valores, strict=False)))
            for clave, valores in zip(self._vista.claves(), self._vista.filas(), strict=True)
        ]
        eliminadas = self._claves_cargadas - {f.id for f in filas if f.id is not None}
        if eliminadas and not self._vista.confirmar(
            "Eliminar filas",
            f"Se eliminarán {len(eliminadas)} filas de '{tabla.titulo}'. Si solo quiere dejar de "
            "usarlas, cancele y ponga Activo = N.\n\n¿Eliminarlas definitivamente?",
        ):
            return
        try:
            cambios = tabla.guardar(filas)
        except ParametrizacionInvalidaError as error:
            self._vista.mostrar_errores(error.errores)
            return
        self._vista.mostrar_resultado(
            f"{tabla.titulo}: {cambios.insertadas} nuevas, {cambios.modificadas} modificadas y "
            f"{cambios.eliminadas} eliminadas."
        )
        self.recargar()

    def _hay_cambios(self) -> bool:
        return self._vista.filas() != self._cargadas