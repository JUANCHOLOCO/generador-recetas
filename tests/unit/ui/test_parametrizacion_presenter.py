from collections.abc import Sequence

from recetas.core.application.mantenimiento import (
    CambiosGuardados,
    ColumnaEditable,
    ErrorCelda,
    FilaParametro,
    ParametrizacionInvalidaError,
)
from recetas.core.domain.errors import PersistenciaError
from recetas.ui.parametrizacion.presenter import ParametrizacionPresenter

COLUMNAS = (
    ColumnaEditable("nombre", "Nombre"),
    ColumnaEditable("tipo_facturacion", "Tipo", ("CORRIENTE", "ANTICIPADA", "AMBAS")),
)


class TablaFalsa:
    def __init__(self, titulo: str, filas: list[FilaParametro], falla: bool = False) -> None:
        self.titulo = titulo
        self._filas = filas
        self.falla = falla
        self.guardados: list[list[FilaParametro]] = []

    def columnas(self) -> tuple[ColumnaEditable, ...]:
        return COLUMNAS

    def listar(self) -> list[FilaParametro]:
        return list(self._filas)

    def guardar(self, filas: Sequence[FilaParametro]) -> CambiosGuardados:
        if self.falla:
            raise ParametrizacionInvalidaError(
                [ErrorCelda("Fila 1 › Tipo: inválido", 0, "tipo_facturacion")]
            )
        self.guardados.append(list(filas))
        return CambiosGuardados(insertadas=1)


class VistaFalsa:
    def __init__(self, respuesta: bool = True) -> None:
        self.respuesta = respuesta
        self._filas: list[list[str]] = []
        self._claves: list[int | None] = []
        self.visibles: set[int] | None = None
        self.errores: list[ErrorCelda] = []
        self.mensajes: list[str] = []
        self.preguntas: list[str] = []
        self.seleccionada: int | None = None

    def mostrar_tabla(
        self,
        columnas: Sequence[ColumnaEditable],
        filas: Sequence[list[str]],
        claves: Sequence[int | None],
    ) -> None:
        self._filas = [list(f) for f in filas]
        self._claves = list(claves)

    def filas(self) -> list[list[str]]:
        return [list(f) for f in self._filas]

    def claves(self) -> list[int | None]:
        return list(self._claves)

    def mostrar_solo(self, visibles: set[int] | None) -> None:
        self.visibles = visibles

    def seleccionar_tabla(self, indice: int) -> None:
        self.seleccionada = indice

    def mostrar_errores(self, errores: Sequence[ErrorCelda]) -> None:
        self.errores = list(errores)

    def confirmar(self, titulo: str, texto: str) -> bool:
        self.preguntas.append(titulo)
        return self.respuesta

    def mostrar_resultado(self, mensaje: str) -> None:
        self.mensajes.append(mensaje)

    # Simula ediciones del usuario
    def editar(self, fila: int, columna: int, valor: str) -> None:
        self._filas[fila][columna] = valor

    def quitar(self, fila: int) -> None:
        del self._filas[fila]
        del self._claves[fila]

    def mostrar_error(self, mensaje: str) -> None:
        self.mensajes.append(f"ERROR: {mensaje}")


def _canales() -> TablaFalsa:
    return TablaFalsa(
        "Canales",
        [
            FilaParametro(1, {"nombre": "Retail", "tipo_facturacion": "CORRIENTE"}),
            FilaParametro(2, {"nombre": "Pyme", "tipo_facturacion": "ANTICIPADA"}),
            FilaParametro(3, {"nombre": "Ecommerce", "tipo_facturacion": "AMBAS"}),
        ],
    )


def _presenter(vista: VistaFalsa, *tablas: TablaFalsa) -> ParametrizacionPresenter:
    presenter = ParametrizacionPresenter(vista, tablas or (_canales(),))
    presenter.recargar()
    return presenter


def test_recargar_muestra_filas_con_sus_ids() -> None:
    vista = VistaFalsa()

    _presenter(vista)

    assert vista.filas()[0] == ["Retail", "CORRIENTE"]
    assert vista.claves() == [1, 2, 3]


def test_filtrar_oculta_pero_conserva_las_filas_de_otro_tipo() -> None:
    vista = VistaFalsa()
    presenter = _presenter(vista)

    presenter.filtrar("CORRIENTE")

    assert vista.visibles == {0, 2}  # CORRIENTE y AMBAS
    assert len(vista.filas()) == 3


def test_guardar_envia_todas_las_filas_aunque_haya_filtro() -> None:
    vista, tabla = VistaFalsa(), _canales()
    presenter = _presenter(vista, tabla)
    presenter.filtrar("CORRIENTE")

    presenter.guardar()

    assert [f.id for f in tabla.guardados[0]] == [1, 2, 3]
    assert vista.mensajes == ["Canales: 1 nuevas, 0 modificadas y 0 eliminadas."]


def test_eliminar_pide_confirmacion_y_si_se_cancela_no_guarda() -> None:
    vista, tabla = VistaFalsa(respuesta=False), _canales()
    presenter = _presenter(vista, tabla)
    vista.quitar(1)

    presenter.guardar()

    assert vista.preguntas == ["Eliminar filas"]
    assert tabla.guardados == []


def test_errores_de_validacion_se_muestran() -> None:
    vista = VistaFalsa()
    tabla = _canales()
    tabla.falla = True
    presenter = _presenter(vista, tabla)

    presenter.guardar()

    assert vista.errores[0].columna == "tipo_facturacion"


def test_cambiar_de_tabla_con_cambios_pide_confirmacion() -> None:
    vista = VistaFalsa(respuesta=False)
    presenter = _presenter(vista, _canales(), TablaFalsa("Roles", []))
    vista.editar(0, 0, "Retail 2")

    presenter.abrir(1)

    assert vista.preguntas == ["Cambios sin guardar"]
    assert vista.seleccionada == 0  # el selector vuelve a la tabla actual
    assert vista.filas()[0][0] == "Retail 2"  # no se descartó lo editado


class TablaQueNoLee(TablaFalsa):
    def listar(self) -> list[FilaParametro]:
        raise PersistenciaError("No se pudo leer la tabla: error de la base de datos.")


def test_error_al_leer_la_tabla_se_muestra() -> None:
    vista = VistaFalsa()

    _presenter(vista, TablaQueNoLee("Canales", []))

    assert vista.mensajes == ["ERROR: No se pudo leer la tabla: error de la base de datos."]
