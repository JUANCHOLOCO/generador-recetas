"""Lógica del formulario de alza de planes pospago (patrón MVP, sin Qt)."""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from pydantic import ValidationError

from recetas.core.application.ports import BundleWriter, LectorDeHojas, Preferencias
from recetas.core.domain.errors import RecetaExistenteError, RecetasError
from recetas.core.domain.importacion import FormatoHoja
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.modules.alza_tarifas.application.generar_alza import AlzaGenerada
from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPlanes


@dataclass(frozen=True, slots=True)
class Columna:
    campo: str  # campo de PlanAlza
    titulo: str  # título en la tabla y en el Excel
    ayuda: str  # tooltip del encabezado


COLUMNAS = (
    Columna("id", "Id", "Id del plan en ACTIVATOR.PLANS (numérico, ej. 1208)"),
    Columna("part_num", "Part_num", "PLCON#### (ej. PLCON0335)"),
    Columna("nombre", "Nombre", "Nombre del plan (solo para el comentario del script)"),
    Columna("precio_nuevo", "Precio nuevo", "ITEM_PRICE y VENDOR_VALUE del aplica (ej. 68083)"),
    Columna("prorrateo_nuevo", "Prorrateo nuevo", "ITEM_PRICE_PRORRATE del aplica"),
    Columna("precio_actual", "Precio actual", "ITEM_PRICE y VENDOR_VALUE del rollback"),
    Columna("prorrateo_actual", "Prorrateo actual", "ITEM_PRICE_PRORRATE del rollback"),
)
_INDICE_COLUMNA = {c.campo: i for i, c in enumerate(COLUMNAS)}
# El Excel trae los mismos títulos de la tabla en la fila 1
FORMATO_EXCEL = FormatoHoja(encabezados=tuple(c.titulo for c in COLUMNAS))
# Mismas claves que Creación de planes: el autor y la carpeta se comparten entre módulos
CLAVE_AUTOR = "autor"
CLAVE_CARPETA = "carpeta_salida"
_ETIQUETAS = {
    "requerimiento": "Número de requerimiento",
    "autor": "Autor",
    "ambiente": "Ambiente",
    "planes": "Planes",
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
    def cargar_planes(self, filas: Sequence[Sequence[str]]) -> None: ...
    def confirmar_limpieza(self) -> bool: ...
    def limpiar(self) -> None: ...
    def mostrar_receta_generada(self, raiz: Path) -> None: ...


class CasoGenerarAlza(Protocol):
    def ejecutar(self, solicitud: SolicitudAlzaPlanes) -> AlzaGenerada: ...


class FormularioAlzaPresenter:
    def __init__(
        self,
        vista: VistaAlza,
        generar_alza: CasoGenerarAlza,
        escritor: BundleWriter,
        lector: LectorDeHojas,
        preferencias: Preferencias,
    ) -> None:
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
        try:
            filas = self._lector.leer(ruta, FORMATO_EXCEL)
        except RecetasError as error:
            self._vista.mostrar_error(str(error))
            return
        if not filas:
            self._vista.mostrar_resultado(f"'{ruta.name}' no trae planes. El formulario no cambió.")
            return

        if _hay_planes(filas_actuales) and not self._vista.confirmar_reemplazo(len(filas)):
            return

        self._vista.cargar_planes(filas)
        self._vista.mostrar_errores([])
        self._vista.mostrar_resultado(
            f"Se importaron {len(filas)} planes de '{ruta.name}'. Revíselos y pulse Generar receta."
        )

    def limpiar(self, datos: DatosAlza) -> None:
        hay_datos = bool(datos.requerimiento.strip()) or _hay_planes(datos.filas)
        if hay_datos and not self._vista.confirmar_limpieza():
            return
        self._vista.limpiar()

    def _validar(self, datos: DatosAlza) -> tuple[SolicitudAlzaPlanes, list[int]] | None:
        errores: list[ErrorCampo] = []
        if not datos.carpeta.strip():
            errores.append(ErrorCampo("Seleccione la carpeta de salida."))
        diccionario, filas_usadas = construir_solicitud(datos)
        solicitud = None
        try:
            solicitud = SolicitudAlzaPlanes.model_validate(diccionario)
        except ValidationError as error:
            errores.extend(errores_legibles(error, filas_usadas))
        self._vista.mostrar_errores(errores)
        if errores or solicitud is None:
            return None
        return solicitud, filas_usadas

    def _escribir(self, bundle: RecipeBundle, carpeta: Path) -> Path | None:
        try:
            return self._escritor.escribir(bundle, carpeta)
        except RecetaExistenteError as error:
            if not self._vista.confirmar_sobrescritura(error.rutas):
                return None
            return self._escritor.escribir(bundle, carpeta, sobrescribir=True)
        except OSError as error:
            self._vista.mostrar_error(f"No se pudo escribir la receta: {error}")
            return None


def construir_solicitud(datos: DatosAlza) -> tuple[dict[str, Any], list[int]]:
    """Convierte el formulario en el diccionario que valida Pydantic.

    Devuelve también qué fila de la tabla corresponde a cada plan, porque las filas
    vacías se ignoran y los índices de Pydantic no coinciden con los de la tabla.
    """
    planes: list[dict[str, str]] = []
    filas_usadas: list[int] = []
    for indice, fila in enumerate(datos.filas):
        if not any(valor.strip() for valor in fila):
            continue
        planes.append({c.campo: valor for c, valor in zip(COLUMNAS, fila, strict=False)})
        filas_usadas.append(indice)
    return (
        {
            "requerimiento": datos.requerimiento,
            "autor": datos.autor,
            "ambiente": datos.ambiente,
            "planes": planes,
        },
        filas_usadas,
    )


def errores_legibles(error: ValidationError, filas_usadas: Sequence[int]) -> list[ErrorCampo]:
    resultado = []
    for detalle in error.errors():
        mensaje = _TRADUCCIONES.get(detalle["type"], detalle["msg"])
        loc = detalle["loc"]
        if len(loc) >= 2 and loc[0] == "planes" and isinstance(loc[1], int):
            fila = filas_usadas[loc[1]]
            columna = _INDICE_COLUMNA.get(".".join(str(parte) for parte in loc[2:]))
            donde = f" › {COLUMNAS[columna].titulo}" if columna is not None else ""
            resultado.append(ErrorCampo(f"Fila {fila + 1}{donde}: {mensaje}", fila, columna))
        else:
            campo = ".".join(str(parte) for parte in loc)
            etiqueta = _ETIQUETAS.get(campo, campo)
            resultado.append(ErrorCampo(f"{etiqueta}: {mensaje}" if etiqueta else mensaje))
    return resultado


def _en_la_tabla(mensaje: str, plan: int | None, filas_usadas: Sequence[int]) -> str:
    """La advertencia numera los planes desde 1; la tabla puede tener filas vacías en medio."""
    return f"Fila {filas_usadas[plan - 1] + 1}: {mensaje}" if plan else mensaje


def _hay_planes(filas: Sequence[Sequence[str]]) -> bool:
    return any(valor.strip() for fila in filas for valor in fila)
