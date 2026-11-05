"""Tipos validados del formulario de alza: formato, longitud y precios."""

import re
from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, StringConstraints
from pydantic_core import PydanticCustomError

from recetas.core.domain.texto import caracteres_fuera_de_cp1252, tiene_caracteres_de_control

MAX_REQUERIMIENTO = 30
MAX_AUTOR = 100
MAX_NOMBRE = 100
MAX_ID = 10
_PRECIO = re.compile(r"\d{1,12}(?:[.,]\d{1,2})?")


def _formato(patron: str, ejemplo: str) -> AfterValidator:
    regex = re.compile(patron)

    def validar(valor: str) -> str:
        if not regex.fullmatch(valor):
            raise PydanticCustomError(
                "formato_invalido", "Debe tener el formato {ejemplo}.", {"ejemplo": ejemplo}
            )
        return valor

    return AfterValidator(validar)


def _maximo(longitud: int) -> AfterValidator:
    def validar(valor: str) -> str:
        if len(valor) > longitud:
            raise PydanticCustomError(
                "demasiado_largo",
                "Máximo {maximo} caracteres (tiene {actual}).",
                {"maximo": longitud, "actual": len(valor)},
            )
        return valor

    return AfterValidator(validar)


def _sin_caracteres_de_control(valor: str) -> str:
    if tiene_caracteres_de_control(valor):
        raise PydanticCustomError(
            "caracteres_de_control", "No puede contener saltos de línea ni tabuladores."
        )
    return valor


def _solo_windows_1252(valor: str) -> str:
    if caracteres := caracteres_fuera_de_cp1252(valor):
        raise PydanticCustomError(
            "fuera_de_windows_1252",
            "Tiene caracteres que el script no admite: {caracteres}. Bórrelos o reemplácelos.",
            {"caracteres": caracteres},
        )
    return valor


def _obligatorio(valor: str) -> str:
    if not valor:
        raise PydanticCustomError("obligatorio", "Es obligatorio.")
    return valor


def _a_precio(valor: object) -> object:
    """'10605,04' o '10605.04' → Decimal('10605.04'). No calcula nada: se escribe tal cual."""
    if isinstance(valor, Decimal):
        return valor
    texto = str(valor).strip()
    if not texto:
        raise PydanticCustomError("obligatorio", "Es obligatorio.")
    if not _PRECIO.fullmatch(texto):
        raise PydanticCustomError(
            "precio_invalido",
            "Debe ser un número mayor o igual a 0, con máximo 2 decimales (ej. 68083 o 10605,04).",
        )
    return Decimal(texto.replace(",", "."))


_Texto = Annotated[
    str,
    StringConstraints(strip_whitespace=True),
    AfterValidator(_sin_caracteres_de_control),
    AfterValidator(_solo_windows_1252),
]
TextoObligatorio = Annotated[_Texto, AfterValidator(_obligatorio)]

Requerimiento = Annotated[
    _Texto,
    _maximo(MAX_REQUERIMIENTO),
    _formato(r"[A-Za-z0-9_-]+", "letras, números, '-' o '_' (ej. TPFB-1726)"),
]
Autor = Annotated[TextoObligatorio, _maximo(MAX_AUTOR)]
Nombre = Annotated[TextoObligatorio, _maximo(MAX_NOMBRE)]
IdNumerico = Annotated[TextoObligatorio, _maximo(MAX_ID), _formato(r"\d+", "numérico (ej. 1208)")]
PartNumPlan = Annotated[TextoObligatorio, _formato(r"PLCON\d{4}", "PLCON#### (ej. PLCON0335)")]
PartNumPaquete = Annotated[TextoObligatorio, _formato(r"SVALL\d{4}", "SVALL#### (ej. SVALL2322)")]
Precio = Annotated[Decimal, BeforeValidator(_a_precio)]


def sql_numero(valor: Decimal) -> str:
    """Número para el script: sin comillas y con punto decimal (10605.04)."""
    return format(valor, "f")
