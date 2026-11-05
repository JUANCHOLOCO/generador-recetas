"""Lógica del formulario de alza de tarifas, común a los dos tipos (patrón MVP, sin Qt)."""

from collections.abc import Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from pydantic import BaseModel, ValidationError

from recetas.core.application.ports import BundleWriter, LectorDeHojas, Preferencias
from recetas.core.domain.errors import RecetaExistenteError, RecetasError
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.modules.alza_tarifas.application.generar_alza import AlzaGenerada
from recetas.modules.alza_tarifas.ui.tipos_formulario import TipoFormulario

# Mismas claves que Creación de planes: el autor y la carpeta se comparten entre módulos
CLAVE_AUTOR = "autor"
CLAVE_CARPETA = "carpeta_salida"
_ETIQUETAS = {
    "requerimiento": "Número de requerimiento",
    "autor": "Autor",
    "ambiente": "Ambiente",
}
_TRADUCCIONES = {
    "missing": "Es obligatorio.",
    "enum": "Seleccione una opción válida.",
}


@dataclass(frozen=True, slots=True)
class DatosAlza:
    """Lo que el usuario escribió, tal cual (todo texto)."""

    requerimiento: str
    autor: str
    ambiente: str
    carpeta: str
    filas: list[list[str]]


@dataclass(frozen=True, slots=True)
class ErrorCampo:
    mensaje: str
    fila: int | None = None  # índice de la fila en la tabla (desde 0)
    columna: int | None = None


class VistaAlza(Protocol):
    def mostrar_errores(self, errores: Sequence[ErrorCampo]) -> None: ...
    def confirmar_advertencias(self, lineas: Sequence[str]) -> bool: ...
    def confirmar_sobrescritura(self, rutas: Sequence[str]) -> bool: ...
    def mostrar_resultado(self, mensaje: str) -> None: ...
    def mostrar_error(self, mensaje: str) -> None: ...
    def confirmar_reemplazo(self, cantidad: int) -> bool: ...
    def cargar_filas(self, filas: Sequence[Sequence[str]]) -> None: ...
    def confirmar_limpieza(self) -> bool: ...
    def limpiar(self) -> None: ...
    def mostrar_receta_generada(self, raiz: Path) -> None: ...
    def trabajando(self) -> AbstractContextManager[None]: ...


class CasoGenerarAlza[S: BaseModel](Protocol):
    def ejecutar(self, solicitud: S) -> AlzaGenerada: ...


class FormularioAlzaPresenter[S: BaseModel]:
    def __init__(
        self,
        tipo: TipoFormulario[S],
        vista: VistaAlza,
        generar_alza: CasoGenerarAlza[S],
        escritor: BundleWriter,
        lector: LectorDeHojas,
        preferencias: Preferencias,
    ) -> None:
        self._tipo = tipo
        self._vista = vista
        self._generar_alza = generar_alza
        self._escritor = escritor
        self._lector = lector
        self._preferencias = preferencias

    def generar(self, datos: DatosAlza) -> None:
        validada = self._validar(datos)
        if validada is None:
            return
        solicitud, filas_usadas = validada

        try:
            with self._vista.trabajando():
                alza = self._generar_alza.ejecutar(solicitud)
        except RecetasError as error:
            self._vista.mostrar_error(str(error))
            return

        lineas = [_en_la_tabla(a.mensaje, a.fila, filas_usadas) for a in alza.advertencias]
        if lineas and not self._vista.confirmar_advertencias(lineas):
            return

        raiz = self._escribir(alza.bundle, Path(datos.carpeta))
        if raiz is None:
            return
        self._preferencias.guardar(CLAVE_AUTOR, datos.autor.strip())
        self._preferencias.guardar(CLAVE_CARPETA, datos.carpeta.strip())
        self._vista.mostrar_receta_generada(raiz)

    def importar(self, ruta: Path, filas_actuales: Sequence[Sequence[str]]) -> None:
        lista = self._tipo.lista
        try:
            filas = self._lector.leer(ruta, self._tipo.formato_excel)
        except RecetasError as error:
            self._vista.mostrar_error(str(error))
            return
        if not filas:
            self._vista.mostrar_resultado(
                f"'{ruta.name}' no trae {lista}. El formulario no cambió."
            )
            return

        if _hay_datos(filas_actuales) and not self._vista.confirmar_reemplazo(len(filas)):
            return

        self._vista.cargar_filas(filas)
        self._vista.mostrar_errores([])
        self._vista.mostrar_resultado(
            f"Se importaron {len(filas)} {lista} de '{ruta.name}'. "
            "Revíselos y pulse Generar receta."
        )

    def limpiar(self, datos: DatosAlza) -> None:
        hay_datos = bool(datos.requerimiento.strip()) or _hay_datos(datos.filas)
        if hay_datos and not self._vista.confirmar_limpieza():
            return
        self._vista.limpiar()

    def _validar(self, datos: DatosAlza) -> tuple[S, list[int]] | None:
        errores: list[ErrorCampo] = []
        if not datos.carpeta.strip():
            errores.append(ErrorCampo("Seleccione la carpeta de salida."))
        diccionario, filas_usadas = construir_solicitud(self._tipo, datos)
        solicitud: S | None = None
        try:
            solicitud = self._tipo.modelo.model_validate(diccionario)
        except ValidationError as error:
            errores.extend(errores_legibles(self._tipo, error, filas_usadas))
        self._vista.mostrar_errores(errores)
        if errores or solicitud is None:
            return None
        return solicitud, filas_usadas

    def _escribir(self, bundle: RecipeBundle, carpeta: Path) -> Path | None:
        try:
            with self._vista.trabajando():
                return self._escritor.escribir(bundle, carpeta)
        except RecetaExistenteError as error:
            if not self._vista.confirmar_sobrescritura(error.rutas):
                return None
            with self._vista.trabajando():
                return self._escritor.escribir(bundle, carpeta, sobrescribir=True)
        except OSError as error:
            self._vista.mostrar_error(f"No se pudo escribir la receta: {error}")
            return None


def construir_solicitud(
    tipo: TipoFormulario[Any], datos: DatosAlza
) -> tuple[dict[str, Any], list[int]]:
    """Convierte el formulario en el diccionario que valida Pydantic.

    Devuelve también qué fila de la tabla corresponde a cada elemento, porque las filas
    vacías se ignoran y los índices de Pydantic no coinciden con los de la tabla.
    """
    elementos: list[dict[str, str]] = []
    filas_usadas: list[int] = []
    for indice, fila in enumerate(datos.filas):
        if not any(valor.strip() for valor in fila):
            continue
        elementos.append({c.campo: valor for c, valor in zip(tipo.columnas, fila, strict=False)})
        filas_usadas.append(indice)
    return (
        {
            "requerimiento": datos.requerimiento,
            "autor": datos.autor,
            "ambiente": datos.ambiente,
            tipo.lista: elementos,
        },
        filas_usadas,
    )


def errores_legibles(
    tipo: TipoFormulario[Any], error: ValidationError, filas_usadas: Sequence[int]
) -> list[ErrorCampo]:
    etiquetas = _ETIQUETAS | {tipo.lista: tipo.lista.capitalize()}
    resultado = []
    for detalle in error.errors():
        mensaje = _TRADUCCIONES.get(detalle["type"], detalle["msg"])
        loc = detalle["loc"]
        if len(loc) >= 2 and loc[0] == tipo.lista and isinstance(loc[1], int):
            fila = filas_usadas[loc[1]]
            columna = tipo.indice(".".join(str(parte) for parte in loc[2:]))
            donde = f" › {tipo.columnas[columna].titulo}" if columna is not None else ""
            resultado.append(ErrorCampo(f"Fila {fila + 1}{donde}: {mensaje}", fila, columna))
        else:
            campo = ".".join(str(parte) for parte in loc)
            etiqueta = etiquetas.get(campo, campo)
            resultado.append(ErrorCampo(f"{etiqueta}: {mensaje}" if etiqueta else mensaje))
    return resultado


def _en_la_tabla(mensaje: str, elemento: int | None, filas_usadas: Sequence[int]) -> str:
    """La advertencia numera los elementos desde 1; la tabla puede tener filas vacías en medio."""
    return f"Fila {filas_usadas[elemento - 1] + 1}: {mensaje}" if elemento else mensaje


def _hay_datos(filas: Sequence[Sequence[str]]) -> bool:
    return any(valor.strip() for fila in filas for valor in fila)
