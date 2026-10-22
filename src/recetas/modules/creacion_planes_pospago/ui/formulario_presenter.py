"""Lógica del formulario de creación de planes (patrón MVP, sin Qt)."""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from pydantic import ValidationError

from recetas.core.application.ports import BundleWriter
from recetas.core.domain.errors import RecetaExistenteError, RecetasError
from recetas.modules.creacion_planes_pospago.application.generar_receta import RecetaGenerada
from recetas.modules.creacion_planes_pospago.application.ports import RegistroDePlanes
from recetas.modules.creacion_planes_pospago.domain.advertencias import Advertencia
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta


@dataclass(frozen=True, slots=True)
class Columna:
    campo: str  # ruta del campo en PlanNuevo; "datos.svall" = campo svall del paquete de datos
    titulo: str


COLUMNAS = (
    Columna("id_plan", "Id_Plan"),
    Columna("part_num", "Part_num"),
    Columna("nombre", "Nombre del producto"),
    Columna("valor_con_iva", "Valor con IVA"),
    Columna("valor_sin_iva", "Valor sin IVA"),
    Columna("codigo_pcrf", "Código perfil PCRF"),
    Columna("tarif_group", "Tarif group"),
    Columna("es_53", "Es 5.3 (S/N)"),
    Columna("datos.nombre", "Nombre paquete Datos"),
    Columna("datos.svall", "Svall Datos"),
    Columna("datos.poid", "POID Datos"),
    Columna("sms.nombre", "Nombre paquete SMS"),
    Columna("sms.svall", "Svall SMS"),
    Columna("sms.poid", "POID SMS"),
)
_INDICE_COLUMNA = {c.campo: i for i, c in enumerate(COLUMNAS)}
_ETIQUETAS = {
    "requerimiento": "Número de requerimiento",
    "autor": "Autor",
    "ambiente": "Ambiente",
    "tipo": "Tipo de facturación",
    "planes": "Planes",
}
_TRADUCCIONES = {
    "missing": "Es obligatorio.",
    "int_parsing": "Debe ser un número entero.",
    "bool_parsing": "Use S o N.",
    "enum": "Seleccione una opción válida.",
}
_SI = {"S", "SI", "SÍ", "X"}
_NO = {"N", "NO", ""}


@dataclass(frozen=True, slots=True)
class DatosFormulario:
    """Lo que el usuario escribió, tal cual (todo texto)."""

    requerimiento: str
    autor: str
    ambiente: str
    tipo: str
    carpeta: str
    filas: list[list[str]]


@dataclass(frozen=True, slots=True)
class ErrorCampo:
    mensaje: str
    fila: int | None = None  # índice de la fila en la tabla (desde 0)
    columna: int | None = None


class VistaFormulario(Protocol):
    def mostrar_errores(self, errores: Sequence[ErrorCampo]) -> None: ...
    def confirmar_advertencias(self, advertencias: Sequence[Advertencia]) -> bool: ...
    def confirmar_sobrescritura(self, rutas: Sequence[str]) -> bool: ...
    def confirmar_registro(self, cantidad: int) -> bool: ...
    def mostrar_resultado(self, mensaje: str) -> None: ...
    def mostrar_error(self, mensaje: str) -> None: ...


class CasoGenerarReceta(Protocol):
    def ejecutar(self, solicitud: SolicitudReceta) -> RecetaGenerada: ...


class FormularioPresenter:
    def __init__(
        self,
        vista: VistaFormulario,
        generar_receta: CasoGenerarReceta,
        escritor: BundleWriter,
        registro: RegistroDePlanes,
    ) -> None:
        self._vista = vista
        self._generar_receta = generar_receta
        self._escritor = escritor
        self._registro = registro

    def generar(self, datos: DatosFormulario) -> None:
        solicitud = self._validar(datos)
        if solicitud is None:
            return

        try:
            receta = self._generar_receta.ejecutar(solicitud)
        except RecetasError as error:
            self._vista.mostrar_error(str(error))
            return

        if receta.advertencias and not self._vista.confirmar_advertencias(receta.advertencias):
            return

        raiz = self._escribir(receta, Path(datos.carpeta))
        if raiz is None:
            return
        self._vista.mostrar_resultado(f"Receta generada en:\n{raiz}")

        if self._vista.confirmar_registro(len(solicitud.planes)):
            registrados = self._registro.registrar(solicitud)
            self._vista.mostrar_resultado(
                f"Planes registrados en la parametrización: {registrados.cambio_plan} en la "
                f"matriz de cambios de plan y {registrados.planes_53} en 5.3 OLDS."
            )

    def _validar(self, datos: DatosFormulario) -> SolicitudReceta | None:
        errores: list[ErrorCampo] = []
        if not datos.carpeta.strip():
            errores.append(ErrorCampo("Seleccione la carpeta de salida."))
        diccionario, filas_usadas = construir_solicitud(datos)
        solicitud = None
        try:
            solicitud = SolicitudReceta.model_validate(diccionario)
        except ValidationError as error:
            errores.extend(errores_legibles(error, filas_usadas))
        self._vista.mostrar_errores(errores)
        return None if errores else solicitud

    def _escribir(self, receta: RecetaGenerada, carpeta: Path) -> Path | None:
        try:
            return self._escritor.escribir(receta.bundle, carpeta)
        except RecetaExistenteError as error:
            if not self._vista.confirmar_sobrescritura(error.rutas):
                return None
            return self._escritor.escribir(receta.bundle, carpeta, sobrescribir=True)
        except OSError as error:
            self._vista.mostrar_error(f"No se pudo escribir la receta: {error}")
            return None


def construir_solicitud(datos: DatosFormulario) -> tuple[dict[str, Any], list[int]]:
    """Convierte el formulario en el diccionario que valida Pydantic.

    Devuelve también qué fila de la tabla corresponde a cada plan, porque las filas
    vacías se ignoran y los índices de Pydantic no coinciden con los de la tabla.
    """
    planes: list[dict[str, Any]] = []
    filas_usadas: list[int] = []
    for indice, fila in enumerate(datos.filas):
        if not any(valor.strip() for valor in fila):
            continue
        plan: dict[str, Any] = {"datos": {}, "sms": {}}
        for columna, valor in zip(COLUMNAS, fila, strict=False):
            destino, _, campo = columna.campo.rpartition(".")
            (plan[destino] if destino else plan)[campo] = valor
        plan["es_53"] = _a_booleano(plan.get("es_53", ""))
        planes.append(plan)
        filas_usadas.append(indice)
    return (
        {
            "requerimiento": datos.requerimiento,
            "autor": datos.autor,
            "ambiente": datos.ambiente,
            "tipo": datos.tipo,
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
            campo = ".".join(str(parte) for parte in loc[2:])
            columna = _INDICE_COLUMNA.get(campo)
            donde = f" › {COLUMNAS[columna].titulo}" if columna is not None else ""
            resultado.append(ErrorCampo(f"Fila {fila + 1}{donde}: {mensaje}", fila, columna))
        else:
            campo = ".".join(str(parte) for parte in loc)
            etiqueta = _ETIQUETAS.get(campo, campo)
            resultado.append(ErrorCampo(f"{etiqueta}: {mensaje}" if etiqueta else mensaje))
    return resultado


def _a_booleano(valor: str) -> bool | str:
    texto = valor.strip().upper()
    if texto in _SI:
        return True
    if texto in _NO:
        return False
    return valor  # Pydantic lo rechazará con 'bool_parsing'