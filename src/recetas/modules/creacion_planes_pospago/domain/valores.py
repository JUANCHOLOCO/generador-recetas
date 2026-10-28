"""Tipos validados del formulario: cada uno sabe qué formato y longitud son válidos."""

import re
from typing import Annotated

from pydantic import AfterValidator, StringConstraints
from pydantic_core import PydanticCustomError

from recetas.core.domain.texto import tiene_caracteres_de_control

# Límites provisionales (docs/ajustes-pendientes.md, U3) hasta conocer las columnas de Oracle.
MAX_REQUERIMIENTO = 30
MAX_AUTOR = 100
MAX_NOMBRE = 100
MAX_CODIGO_PCRF = 50
MAX_ID = 10
MAX_POID = 20


def _formato(patron: str, ejemplo: str) -> AfterValidator:
    """Validador que exige que todo el texto cumpla la expresión regular."""
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


def _obligatorio(valor: str) -> str:
    if not valor:
        raise PydanticCustomError("obligatorio", "Es obligatorio.")
    return valor


def _positivo(valor: int) -> int:
    if valor <= 0:
        raise PydanticCustomError("no_positivo", "Debe ser mayor que cero.")
    return valor


# Todo texto del formulario: sin espacios en los extremos y sin caracteres de control.
_Texto = Annotated[
    str, StringConstraints(strip_whitespace=True), AfterValidator(_sin_caracteres_de_control)
]

TextoObligatorio = Annotated[_Texto, AfterValidator(_obligatorio)]
Nombre = Annotated[TextoObligatorio, _maximo(MAX_NOMBRE)]
Autor = Annotated[TextoObligatorio, _maximo(MAX_AUTOR)]
Requerimiento = Annotated[
    _Texto,
    _maximo(MAX_REQUERIMIENTO),
    _formato(r"[A-Za-z0-9_-]+", "letras, números, '-' o '_' (ej. TPFB-2753)"),
]
IdPlan = Annotated[_Texto, _maximo(MAX_ID), _formato(r"\d+", "numérico (ej. 7751)")]
PartNum = Annotated[_Texto, _formato(r"PLCON\d{4}", "PLCON#### (ej. PLCON0454)")]
Svall = Annotated[_Texto, _formato(r"SVALL\d{4}", "SVALL#### (ej. SVALL2632)")]
Poid = Annotated[_Texto, _maximo(MAX_POID), _formato(r"\d+", "numérico (ej. 990000885)")]
TarifGroup = Annotated[_Texto, _maximo(MAX_ID), _formato(r"\d+", "numérico (ej. 120617)")]
CodigoPcrf = Annotated[
    _Texto,
    _maximo(MAX_CODIGO_PCRF),
    _formato(r"\S+", "sin espacios (ej. Conectados_51_FC)"),
]
Valor = Annotated[int, AfterValidator(_positivo)]
