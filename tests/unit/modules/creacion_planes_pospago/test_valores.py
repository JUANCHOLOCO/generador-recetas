from typing import Any

import pytest
from pydantic import TypeAdapter, ValidationError

from recetas.modules.creacion_planes_pospago.domain.valores import (
    IdPlan,
    PartNum,
    Requerimiento,
    Svall,
    TextoObligatorio,
    Valor,
    Autor,
    CodigoPcrf,
    Nombre,
    Poid,
    TarifGroup,
    MAX_REQUERIMIENTO,
    MAX_AUTOR,
    MAX_NOMBRE,
    MAX_CODIGO_PCRF,
    MAX_ID,
    MAX_POID,
)

def validar(tipo: Any, valor: object) -> object:
    return TypeAdapter(tipo).validate_python(valor)


@pytest.mark.parametrize("valor", ["PLCON0454", "  PLCON0454 "])
def test_part_num_valido_y_sin_espacios(valor: str) -> None:
    assert validar(PartNum, valor) == "PLCON0454"


@pytest.mark.parametrize("valor", ["PLCON454", "plcon0454", "SVALL0454", "PLCON04545", ""])
def test_part_num_invalido(valor: str) -> None:
    with pytest.raises(ValidationError, match="PLCON####"):
        validar(PartNum, valor)


@pytest.mark.parametrize("valor", ["SVALL263", "SVALL26320", "PLCON2632"])
def test_svall_invalido(valor: str) -> None:
    with pytest.raises(ValidationError, match="SVALL####"):
        validar(Svall, valor)


def test_id_plan_solo_digitos() -> None:
    assert validar(IdPlan, " 7751 ") == "7751"
    with pytest.raises(ValidationError, match="numérico"):
        validar(IdPlan, "77a1")


def test_requerimiento_sin_espacios_internos() -> None:
    assert validar(Requerimiento, "TPFB-2753") == "TPFB-2753"
    with pytest.raises(ValidationError):
        validar(Requerimiento, "TPFB 2753")


def test_texto_obligatorio_no_acepta_solo_espacios() -> None:
    with pytest.raises(ValidationError, match="Es obligatorio"):
        validar(TextoObligatorio, "   ")


def test_valor_convierte_texto_a_entero_y_exige_positivo() -> None:
    assert validar(Valor, "19900") == 19900
    with pytest.raises(ValidationError, match="mayor que cero"):
        validar(Valor, 0)

@pytest.mark.parametrize("tipo", [TextoObligatorio, Nombre, CodigoPcrf, Requerimiento])
def test_rechaza_saltos_de_linea_y_tabuladores(tipo: Any) -> None:
    for valor in ["Pospago\n/\nConectados", "Pospago\tFC"]:
        with pytest.raises(ValidationError, match="saltos de línea"):
            validar(tipo, valor)


@pytest.mark.parametrize(
    ("tipo", "maximo"),
    [
        (Nombre, MAX_NOMBRE),
        (Autor, MAX_AUTOR),
        (CodigoPcrf, MAX_CODIGO_PCRF),
        (Requerimiento, MAX_REQUERIMIENTO),
    ],
)
def test_longitud_maxima_de_textos(tipo: Any, maximo: int) -> None:
    assert validar(tipo, "A" * maximo) == "A" * maximo
    with pytest.raises(ValidationError, match=f"Máximo {maximo} caracteres"):
        validar(tipo, "A" * (maximo + 1))


@pytest.mark.parametrize(
    ("tipo", "maximo"), [(IdPlan, MAX_ID), (TarifGroup, MAX_ID), (Poid, MAX_POID)]
)
def test_longitud_maxima_de_numericos(tipo: Any, maximo: int) -> None:
    assert validar(tipo, "9" * maximo) == "9" * maximo
    with pytest.raises(ValidationError, match=f"Máximo {maximo} caracteres"):
        validar(tipo, "9" * (maximo + 1))