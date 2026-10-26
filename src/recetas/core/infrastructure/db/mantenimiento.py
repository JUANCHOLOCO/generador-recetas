"""Mantenimiento genérico de una tabla de parametrización (adaptador de TablaMantenible)."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import Boolean, Column, Enum, Integer, String, select
from sqlalchemy import inspect as inspeccionar
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from recetas.core.application.mantenimiento import (
    CambiosGuardados,
    ColumnaEditable,
    ErrorCelda,
    FilaParametro,
    ParametrizacionInvalidaError,
)
from recetas.core.infrastructure.db.base import Base

_SI = {"S", "SI", "SÍ", "X", "1", "TRUE"}
_NO = {"N", "NO", "0", "FALSE"}
_ORDEN = "orden"
_AL_FINAL = ("orden", "tipo_facturacion", "activo")  # columnas de ParametroMixin
_TITULOS = {
    "orden": "Orden",
    "tipo_facturacion": "Tipo de facturación",
    "activo": "Activo (S/N)",
}


class SqlTablaParametrizacion:
    def __init__(
        self, titulo: str, model: type[Base], session_factory: sessionmaker[Session]
    ) -> None:
        self.titulo = titulo
        self._model = model
        self._session_factory = session_factory
        todas = {
            nombre: columna
            for nombre, columna in inspeccionar(model).columns.items()
            if not columna.primary_key
        }
        negocio = [n for n in todas if n not in _AL_FINAL]
        finales = [n for n in _AL_FINAL if n in todas]
        self._columnas: dict[str, Column[Any]] = {n: todas[n] for n in negocio + finales}

    def columnas(self) -> tuple[ColumnaEditable, ...]:
        return tuple(
            ColumnaEditable(nombre, _titulo(nombre), _opciones(columna), _ayuda(nombre, columna))
            for nombre, columna in self._columnas.items()
        )

    def listar(self) -> list[FilaParametro]:
        mapeo = inspeccionar(self._model).columns
        orden = [mapeo[n] for n in (_ORDEN, "id") if n in mapeo]
        with self._session_factory() as session:
            objetos = session.scalars(select(self._model).order_by(*orden)).all()
            return [
                FilaParametro(
                    getattr(objeto, "id"),
                    {n: _a_texto(getattr(objeto, n)) for n in self._columnas},
                )
                for objeto in objetos
            ]

    def guardar(self, filas: Sequence[FilaParametro]) -> CambiosGuardados:
        convertidas, errores = self._convertir(filas)
        if errores:
            raise ParametrizacionInvalidaError(errores)
        try:
            with self._session_factory.begin() as session:
                return self._sincronizar(session, filas, convertidas)
        except IntegrityError:
            raise ParametrizacionInvalidaError(
                [
                    ErrorCelda(
                        "Hay filas repetidas: dos filas tienen la misma combinación que debe ser "
                        "única (por ejemplo, el mismo ID con el mismo tipo de facturación)."
                    )
                ]
            ) from None

    # ---------- Internos ----------

    def _convertir(
        self, filas: Sequence[FilaParametro]
    ) -> tuple[list[dict[str, object]], list[ErrorCelda]]:
        convertidas: list[dict[str, object]] = []
        errores: list[ErrorCelda] = []
        for i, fila in enumerate(filas):
            valores: dict[str, object] = {}
            for nombre, columna in self._columnas.items():
                texto = fila.valores.get(nombre, "").strip()
                if nombre == _ORDEN and not texto:
                    valores[nombre] = None  # se asigna al final de la tabla
                    continue
                try:
                    valores[nombre] = _desde_texto(columna, texto)
                except ValueError as error:
                    errores.append(
                        ErrorCelda(f"Fila {i + 1} › {_titulo(nombre)}: {error}", i, nombre)
                    )
            convertidas.append(valores)
        return convertidas, errores

    def _sincronizar(
        self,
        session: Session,
        filas: Sequence[FilaParametro],
        convertidas: list[dict[str, object]],
    ) -> CambiosGuardados:
        existentes = {getattr(o, "id"): o for o in session.scalars(select(self._model))}
        enviados = {f.id for f in filas if f.id is not None}

        eliminadas = 0
        for id_, objeto in existentes.items():
            if id_ not in enviados:
                session.delete(objeto)
                eliminadas += 1
        session.flush()  # primero se borra, para no chocar con restricciones únicas al reinsertar

        ordenes = [v[_ORDEN] for v in convertidas if isinstance(v.get(_ORDEN), int)]
        siguiente = max(ordenes, default=0)
        insertadas = modificadas = 0
        for fila, valores in zip(filas, convertidas, strict=True):
            if _ORDEN in valores and valores[_ORDEN] is None:
                siguiente += 1
                valores[_ORDEN] = siguiente
            objeto = existentes.get(fila.id) if fila.id is not None else None
            if objeto is None:
                session.add(self._model(**valores))
                insertadas += 1
            elif any(getattr(objeto, k) != v for k, v in valores.items()):
                for k, v in valores.items():
                    setattr(objeto, k, v)
                modificadas += 1
        return CambiosGuardados(insertadas, modificadas, eliminadas)


def _titulo(nombre: str) -> str:
    return _TITULOS.get(nombre, nombre.replace("_", " ").capitalize())


def _opciones(columna: Column[Any]) -> tuple[str, ...]:
    if isinstance(columna.type, Enum):
        return tuple(columna.type.enums)
    if isinstance(columna.type, Boolean):
        return ("S", "N")
    return ()


def _ayuda(nombre: str, columna: Column[Any]) -> str:
    partes = []
    if opciones := _opciones(columna):
        partes.append("Valores: " + ", ".join(opciones))
    if nombre == _ORDEN:
        partes.append("Vacío = al final")
    elif getattr(columna.default, "arg", None) is not None:
        partes.append(f"Vacío = {_a_texto(getattr(columna.default, 'arg'))}")
    return ". ".join(partes)


def _a_texto(valor: object) -> str:
    if valor is None:
        return ""
    if isinstance(valor, bool):
        return "S" if valor else "N"
    return str(valor)


def _desde_texto(columna: Column[Any], texto: str) -> object:
    if not texto:
        defecto = getattr(columna.default, "arg", None)
        if defecto is not None:
            return defecto
        if columna.nullable:
            return None
        raise ValueError("Es obligatorio.")
    tipo = columna.type
    if isinstance(tipo, Boolean):
        if texto.upper() in _SI:
            return True
        if texto.upper() in _NO:
            return False
        raise ValueError("Use S o N.")
    if isinstance(tipo, Enum):
        opciones = list(tipo.enums)
        if texto.upper() not in opciones:
            raise ValueError(f"Use uno de: {', '.join(opciones)}.")
        return tipo.enum_class(texto.upper()) if tipo.enum_class else texto.upper()
    if isinstance(tipo, Integer):
        try:
            return int(texto)
        except ValueError:
            raise ValueError("Debe ser un número entero.") from None
    if isinstance(tipo, String) and tipo.length and len(texto) > tipo.length:
        raise ValueError(f"Máximo {tipo.length} caracteres.")
    return texto