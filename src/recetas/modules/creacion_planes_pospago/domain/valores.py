"""Tipos validados del formulario: cada uno sabe qué formato es válido."""

import re
from collections.abc import Callable
from typing import Annotated

from pydantic import AfterValidator, StringConstraints
from pydantic_core import PydanticCustomError


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


def _obligatorio(valor: str) -> str:
    if not valor:
        raise PydanticCustomError("obligatorio", "Es obligatorio.")
    return valor


def _positivo(valor: int) -> int:
    if valor <= 0:
        raise PydanticCustomError("no_positivo", "Debe ser mayor que cero.")
    return valor


_Texto = Annotated[str, StringConstraints(strip_whitespace=True)]
_Validador = Callable[[str], str]

TextoObligatorio = Annotated[_Texto, AfterValidator(_obligatorio)]
Requerimiento = Annotated[
    _Texto, _formato(r"[A-Za-z0-9_-]+", "letras, números, '-' o '_' (ej. TPFB-2753)")
]
IdPlan = Annotated[_Texto, _formato(r"\d+", "numérico (ej. 7751)")]
PartNum = Annotated[_Texto, _formato(r"PLCON\d{4}", "PLCON#### (ej. PLCON0454)")]
Svall = Annotated[_Texto, _formato(r"SVALL\d{4}", "SVALL#### (ej. SVALL2632)")]
Poid = Annotated[_Texto, _formato(r"\d+", "numérico (ej. 990000885)")]
TarifGroup = Annotated[_Texto, _formato(r"\d+", "numérico (ej. 120617)")]
CodigoPcrf = Annotated[_Texto, _formato(r"\S+", "sin espacios (ej. Conectados_51_FC)")]
Valor = Annotated[int, AfterValidator(_positivo)]