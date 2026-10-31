from collections.abc import Sequence
from pathlib import Path
from typing import Any

from recetas.core.domain.errors import PersistenciaError, RecetaExistenteError, RecetasError
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.modules.creacion_planes_pospago.application.generar_receta import RecetaGenerada
from recetas.modules.creacion_planes_pospago.application.ports import PlanesRegistrados
from recetas.modules.creacion_planes_pospago.domain.advertencias import Advertencia
from recetas.modules.creacion_planes_pospago.domain.plan import SolicitudReceta
from recetas.modules.creacion_planes_pospago.domain.propiedades import (
    ArchivoPropiedades,
    Ubicacion,
)
from recetas.modules.creacion_planes_pospago.ui.formulario_presenter import (
    COLUMNAS,
    DatosFormulario,
    ErrorCampo,
    FormularioPresenter,
)
from tests.factories import datos_plan

# ---------- Dobles de prueba ----------

PROPIEDADES = (
    ArchivoPropiedades("promotions.properties", Ubicacion.WEBLOGIC, ("PLANSPOSPAGO5=,7751",)),
)


class VistaFalsa:
    def __init__(self, respuestas: bool = True) -> None:
        self.respuestas = respuestas
        self.errores: list[ErrorCampo] = []
        self.mensajes: list[str] = []
        self.preguntas: list[str] = []
        self.propiedades: list[ArchivoPropiedades] = []

    def mostrar_errores(self, errores: Sequence[ErrorCampo]) -> None:
        self.errores = list(errores)

    def confirmar_advertencias(self, advertencias: Sequence[Advertencia]) -> bool:
        self.preguntas.append("advertencias")
        return self.respuestas

    def confirmar_sobrescritura(self, rutas: Sequence[str]) -> bool:
        self.preguntas.append("sobrescribir")
        return self.respuestas

    def confirmar_registro(self, cantidad: int) -> bool:
        self.preguntas.append("registrar")
        return self.respuestas

    def mostrar_resultado(self, mensaje: str) -> None:
        self.mensajes.append(mensaje)

    def mostrar_error(self, mensaje: str) -> None:
        self.mensajes.append(f"ERROR: {mensaje}")

    def mostrar_propiedades(self, archivos: Sequence[ArchivoPropiedades]) -> None:
        self.propiedades = list(archivos)


class GeneradorFalso:
    def __init__(self, advertencias: tuple[Advertencia, ...] = (), falla: bool = False) -> None:
        self.advertencias = advertencias
        self.falla = falla
        self.solicitudes: list[SolicitudReceta] = []

    def ejecutar(self, solicitud: SolicitudReceta) -> RecetaGenerada:
        self.solicitudes.append(solicitud)
        if self.falla:
            raise RecetasError("Faltan campos estáticos de PLANS: STATUS.")
        return RecetaGenerada(
            RecipeBundle("TPFB-2753_Prod").add("a.sql", "x"), self.advertencias, PROPIEDADES
        )


class EscritorFalso:
    def __init__(self, existe: bool = False) -> None:
        self.existe = existe
        self.escrituras: list[bool] = []

    def escribir(self, bundle: RecipeBundle, carpeta: Path, *, sobrescribir: bool = False) -> Path:
        if self.existe and not sobrescribir:
            raise RecetaExistenteError([str(carpeta / "TPFB-2753_Prod" / "Corriente")])
        self.escrituras.append(sobrescribir)
        return carpeta / str(bundle.root)


class RegistroFalso:
    def __init__(self, falla: bool = False) -> None:
        self.falla = falla
        self.registradas: list[SolicitudReceta] = []

    def registrar(self, solicitud: SolicitudReceta) -> PlanesRegistrados:
        if self.falla:
            raise PersistenciaError("No se pudo registrar los planes: error de la base de datos.")
        self.registradas.append(solicitud)
        return PlanesRegistrados(cambio_plan=len(solicitud.planes), planes_53=0)


# ---------- Helpers ----------


def fila(**cambios: Any) -> list[str]:
    """Una fila de la tabla con los datos del plan 5.1 FC de TPFB-2753."""
    plano = datos_plan(**cambios)
    valores = []
    for columna in COLUMNAS:
        destino, _, campo = columna.campo.rpartition(".")
        valor = plano[destino][campo] if destino else plano[campo]
        valores.append("N" if valor is False else "S" if valor is True else str(valor))
    return valores


def datos(filas: list[list[str]] | None = None, **cambios: Any) -> DatosFormulario:
    base: dict[str, Any] = {
        "requerimiento": "TPFB-2753",
        "autor": "Equipo Tecnico",
        "ambiente": "PROD",
        "tipo": "CORRIENTE",
        "carpeta": "C:/recetas",
        "filas": filas if filas is not None else [fila()],
    }
    return DatosFormulario(**(base | cambios))


def presenter(
    vista: VistaFalsa,
    generador: GeneradorFalso | None = None,
    escritor: EscritorFalso | None = None,
    registro: RegistroFalso | None = None,
) -> FormularioPresenter:
    return FormularioPresenter(
        vista,
        generador or GeneradorFalso(),
        escritor or EscritorFalso(),
        registro or RegistroFalso(),
    )


# ---------- Validación ----------


def test_formulario_vacio_muestra_errores_generales_y_no_genera() -> None:
    vista, generador = VistaFalsa(), GeneradorFalso()

    presenter(vista, generador).generar(
        datos(filas=[["" for _ in COLUMNAS]], requerimiento="", tipo="", carpeta="")
    )

    mensajes = [e.mensaje for e in vista.errores]
    assert "Seleccione la carpeta de salida." in mensajes
    assert any(m.startswith("Número de requerimiento") for m in mensajes)
    assert any(m.startswith("Tipo de facturación") for m in mensajes)
    assert any("al menos un plan" in m for m in mensajes)
    assert generador.solicitudes == []


def test_error_de_celda_apunta_a_la_fila_real_aunque_haya_filas_vacias() -> None:
    vista = VistaFalsa()
    filas = [["" for _ in COLUMNAS], fila(sms={"nombre": "SMS", "svall": "X", "poid": "1"})]

    presenter(vista).generar(datos(filas=filas))

    [error] = vista.errores
    assert (error.fila, error.columna) == (1, 12)  # fila 2 de la tabla, columna "Svall SMS"
    assert error.mensaje.startswith("Fila 2 › Svall SMS:")


def test_mensajes_nativos_de_pydantic_traducidos() -> None:
    vista = VistaFalsa()

    presenter(vista).generar(datos(filas=[fila(valor_con_iva="abc")]))

    assert vista.errores[0].mensaje == "Fila 1 › Valor con IVA: Debe ser un número entero."


def test_es_53_acepta_s_y_n() -> None:
    generador = GeneradorFalso()

    presenter(VistaFalsa(), generador).generar(datos(filas=[fila(es_53=True)]))

    assert generador.solicitudes[0].planes[0].es_53 is True


# ---------- Flujo de generación ----------


def test_camino_feliz_genera_escribe_y_registra() -> None:
    vista, escritor, registro = VistaFalsa(), EscritorFalso(), RegistroFalso()

    presenter(vista, escritor=escritor, registro=registro).generar(datos())

    assert vista.errores == []
    assert escritor.escrituras == [False]
    assert len(registro.registradas) == 1
    assert "Receta generada en" in vista.mensajes[0]
    assert "1 en la matriz" in vista.mensajes[1]
    assert vista.propiedades == list(PROPIEDADES)


def test_rechazar_advertencias_cancela_sin_escribir() -> None:
    vista, escritor = VistaFalsa(respuestas=False), EscritorFalso()
    generador = GeneradorFalso(advertencias=(Advertencia("Id ya registrado", 1),))

    presenter(vista, generador, escritor).generar(datos())

    assert vista.preguntas == ["advertencias"]
    assert escritor.escrituras == []


def test_receta_existente_pide_confirmacion_y_sobrescribe() -> None:
    vista, escritor = VistaFalsa(), EscritorFalso(existe=True)

    presenter(vista, escritor=escritor).generar(datos())

    assert vista.preguntas[0] == "sobrescribir"
    assert escritor.escrituras == [True]


def test_no_sobrescribir_tampoco_registra() -> None:
    vista, registro = VistaFalsa(respuestas=False), RegistroFalso()

    presenter(vista, escritor=EscritorFalso(existe=True), registro=registro).generar(datos())

    assert vista.preguntas == ["sobrescribir"]
    assert registro.registradas == []
    assert vista.propiedades == []


def test_error_de_negocio_se_muestra_sin_romper_la_app() -> None:
    vista = VistaFalsa()

    presenter(vista, GeneradorFalso(falla=True)).generar(datos())

    assert vista.mensajes == ["ERROR: Faltan campos estáticos de PLANS: STATUS."]


def test_error_al_registrar_se_informa_sin_perder_la_receta_generada() -> None:
    vista = VistaFalsa()

    presenter(vista, registro=RegistroFalso(falla=True)).generar(datos())

    assert "Receta generada en" in vista.mensajes[0]
    assert vista.mensajes[1].startswith("ERROR: La receta se generó, pero no se pudieron registrar")
