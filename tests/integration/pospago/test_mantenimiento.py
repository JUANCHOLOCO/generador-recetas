import pytest
from sqlalchemy.orm import Session, sessionmaker

from recetas.core.application.mantenimiento import (
    CambiosGuardados,
    FilaParametro,
    ParametrizacionInvalidaError,
)
from recetas.core.infrastructure.db.mantenimiento import SqlTablaParametrizacion
from recetas.modules.creacion_planes_pospago.infrastructure.models import (
    CanalModel,
    CplPlanPlanModel,
)

pytestmark = pytest.mark.integration


@pytest.fixture
def canales(session_factory: sessionmaker[Session]) -> SqlTablaParametrizacion:
    return SqlTablaParametrizacion("Canales", CanalModel, session_factory)


@pytest.fixture
def matriz(session_factory: sessionmaker[Session]) -> SqlTablaParametrizacion:
    return SqlTablaParametrizacion("Matriz", CplPlanPlanModel, session_factory)


def _fila(id_: int | None = None, /, **valores: str) -> FilaParametro:
    return FilaParametro(id_, valores)


def test_columnas_por_introspeccion_con_las_de_control_al_final(
    matriz: SqlTablaParametrizacion,
) -> None:
    columnas = {c.nombre: c for c in matriz.columnas()}

    assert list(columnas) == ["id_plan", "lista", "orden", "tipo_facturacion", "activo"]
    assert columnas["tipo_facturacion"].opciones == ("CORRIENTE", "ANTICIPADA", "AMBAS")
    assert columnas["activo"].opciones == ("S", "N")
    assert "Vacío = AMBAS" in columnas["tipo_facturacion"].ayuda


def test_insertar_con_valores_por_defecto_y_orden_al_final(
    canales: SqlTablaParametrizacion,
) -> None:
    cambios = canales.guardar([_fila(nombre="Retail", orden="5"), _fila(nombre="Pyme")])

    assert cambios == CambiosGuardados(insertadas=2)
    assert [f.valores for f in canales.listar()] == [
        {"nombre": "Retail", "orden": "5", "tipo_facturacion": "AMBAS", "activo": "S"},
        {"nombre": "Pyme", "orden": "6", "tipo_facturacion": "AMBAS", "activo": "S"},
    ]


def test_modificar_desactivar_y_eliminar(canales: SqlTablaParametrizacion) -> None:
    canales.guardar([_fila(nombre="Retail"), _fila(nombre="Pyme"), _fila(nombre="Ecommerce")])
    retail, pyme, _ = canales.listar()

    cambios = canales.guardar(
        [
            _fila(retail.id, **(retail.valores | {"activo": "N"})),
            _fila(pyme.id, **pyme.valores),  # sin cambios
        ]
    )

    assert cambios == CambiosGuardados(modificadas=1, eliminadas=1)
    assert [(f.valores["nombre"], f.valores["activo"]) for f in canales.listar()] == [
        ("Retail", "N"),
        ("Pyme", "S"),
    ]


def test_errores_de_validacion_no_guardan_nada(matriz: SqlTablaParametrizacion) -> None:
    filas = [
        _fila(id_plan="7999", lista="NINTENDO", tipo_facturacion="OTRO"),
        _fila(id_plan="", lista="NINTENDO", orden="abc"),
    ]

    with pytest.raises(ParametrizacionInvalidaError) as error:
        matriz.guardar(filas)

    mensajes = [e.mensaje for e in error.value.errores]
    assert any("Tipo de facturación: Use uno de" in m for m in mensajes)
    assert any("Fila 2 › Id plan: Es obligatorio." in m for m in mensajes)
    assert any("Orden: Debe ser un número entero." in m for m in mensajes)
    assert matriz.listar() == []


def test_filas_repetidas_se_reportan_sin_guardar(matriz: SqlTablaParametrizacion) -> None:
    repetida = {"id_plan": "7999", "lista": "NINTENDO", "tipo_facturacion": "CORRIENTE"}

    with pytest.raises(ParametrizacionInvalidaError, match="repetidas"):
        matriz.guardar([_fila(**repetida), _fila(**repetida)])

    assert matriz.listar() == []


def test_salto_de_linea_en_parametrizacion_se_rechaza(canales: SqlTablaParametrizacion) -> None:
    with pytest.raises(ParametrizacionInvalidaError, match="saltos de línea"):
        canales.guardar([_fila(nombre="Retail\n/")])

