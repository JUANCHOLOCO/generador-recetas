from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from recetas.core.domain.errors import ImportacionError, RecetaExistenteError, RecetasError
from recetas.core.domain.importacion import FormatoHoja
from recetas.core.domain.recipe_bundle import RecipeBundle
from recetas.modules.alza_tarifas.application.generar_alza import AlzaGenerada
from recetas.modules.alza_tarifas.domain.advertencias import Advertencia
from recetas.modules.alza_tarifas.domain.solicitud import SolicitudAlzaPaquetes
from recetas.modules.alza_tarifas.ui.formulario_presenter import (
    CLAVE_AUTOR,
    CLAVE_CARPETA,
    DatosAlza,
    ErrorCampo,
    FormularioAlzaPresenter,
)
from recetas.modules.alza_tarifas.ui.tipos_formulario import PAQUETES, PLANES, TipoFormulario
from tests.factories import datos_paquete_alza, datos_plan_alza

# ---------- Dobles de prueba ----------


class VistaFalsa:
    def __init__(self, respuestas: bool = True) -> None:
        self.respuestas = respuestas
        self.errores: list[ErrorCampo] = []
        self.mensajes: list[str] = []
        self.preguntas: list[str] = []
        self.advertencias: list[str] = []
        self.cargadas: list[list[str]] | None = None
        self.limpiado = False
        self.trabajos = 0

    def mostrar_errores(self, errores: Sequence[ErrorCampo]) -> None:
        self.errores = list(errores)

    def confirmar_advertencias(self, lineas: Sequence[str]) -> bool:
        self.preguntas.append("advertencias")
        self.advertencias = list(lineas)
        return self.respuestas

    def confirmar_sobrescritura(self, rutas: Sequence[str]) -> bool:
        self.preguntas.append("sobrescribir")
        return self.respuestas

    def mostrar_resultado(self, mensaje: str) -> None:
        self.mensajes.append(mensaje)

    def mostrar_error(self, mensaje: str) -> None:
        self.mensajes.append(f"ERROR: {mensaje}")

    def confirmar_reemplazo(self, cantidad: int) -> bool:
        self.preguntas.append("reemplazar")
        return self.respuestas

    def cargar_filas(self, filas: Sequence[Sequence[str]]) -> None:
        self.cargadas = [list(f) for f in filas]

    def confirmar_limpieza(self) -> bool:
        self.preguntas.append("limpiar")
        return self.respuestas

    def limpiar(self) -> None:
        self.limpiado = True

    def mostrar_receta_generada(self, raiz: Path) -> None:
        self.mensajes.append(f"Receta generada en:\n{raiz}")

    @contextmanager
    def trabajando(self) -> Iterator[None]:
        self.trabajos += 1
        yield


class GeneradorFalso:
    def __init__(self, advertencias: tuple[Advertencia, ...] = (), falla: bool = False) -> None:
        self.advertencias = advertencias
        self.falla = falla
        self.solicitudes: list[BaseModel] = []

    def ejecutar(self, solicitud: BaseModel) -> AlzaGenerada:
        self.solicitudes.append(solicitud)
        if self.falla:
            raise RecetasError("No se pudo generar el alza.")
        return AlzaGenerada(RecipeBundle("TPFB-1726_Prod").add("a.sql", "x"), self.advertencias)


class EscritorFalso:
    def __init__(self, existe: bool = False) -> None:
        self.existe = existe
        self.escrituras: list[bool] = []

    def escribir(self, bundle: RecipeBundle, carpeta: Path, *, sobrescribir: bool = False) -> Path:
        if self.existe and not sobrescribir:
            raise RecetaExistenteError([str(carpeta / "TPFB-1726_Prod" / "AlzaPlanesPospago")])
        self.escrituras.append(sobrescribir)
        return carpeta / str(bundle.root)


class LectorFalso:
    def __init__(self, filas: list[list[str]] | None = None, falla: bool = False) -> None:
        self.filas = filas
        self.falla = falla
        self.formatos: list[FormatoHoja] = []

    def leer(self, ruta: Path, formato: FormatoHoja) -> list[list[str]]:
        self.formatos.append(formato)
        if self.falla:
            raise ImportacionError("No se pudo leer 'alza.xlsx'.")
        return self.filas if self.filas is not None else [fila()]


class PreferenciasEnMemoria:
    def __init__(self) -> None:
        self.valores: dict[str, str] = {}

    def leer(self, clave: str) -> str | None:
        return self.valores.get(clave)

    def guardar(self, clave: str, valor: str) -> None:
        self.valores[clave] = valor


# ---------- Helpers ----------

VACIO = [[""] * len(PLANES.columnas)]


def fila(**cambios: Any) -> list[str]:
    """Una fila de la tabla con el plan 'Pospago 5.1 Empresarial' de TPFB-1726."""
    plano = datos_plan_alza(**cambios)
    return [str(plano[c.campo]) for c in PLANES.columnas]


def datos(filas: list[list[str]] | None = None, **cambios: Any) -> DatosAlza:
    base: dict[str, Any] = {
        "requerimiento": "TPFB-1726",
        "autor": "Equipo Tecnico",
        "ambiente": "PROD",
        "carpeta": "C:/recetas",
        "filas": filas if filas is not None else [fila()],
    }
    return DatosAlza(**(base | cambios))


def presenter(
    vista: VistaFalsa,
    generador: GeneradorFalso | None = None,
    escritor: EscritorFalso | None = None,
    lector: LectorFalso | None = None,
    preferencias: PreferenciasEnMemoria | None = None,
    tipo: TipoFormulario[Any] = PLANES,
) -> FormularioAlzaPresenter[Any]:
    return FormularioAlzaPresenter(
        tipo,
        vista,
        generador or GeneradorFalso(),
        escritor or EscritorFalso(),
        lector or LectorFalso(),
        preferencias or PreferenciasEnMemoria(),
    )


# ---------- Validación ----------


def test_formulario_vacio_muestra_errores_generales_y_no_genera() -> None:
    vista, generador = VistaFalsa(), GeneradorFalso()

    presenter(vista, generador).generar(datos(filas=VACIO, requerimiento="", carpeta=""))

    mensajes = [e.mensaje for e in vista.errores]
    assert "Seleccione la carpeta de salida." in mensajes
    assert any(m.startswith("Número de requerimiento") for m in mensajes)
    assert "Planes: Debe agregar al menos un plan." in mensajes
    assert generador.solicitudes == []


def test_error_de_celda_apunta_a_la_fila_real_aunque_haya_filas_vacias() -> None:
    vista = VistaFalsa()

    presenter(vista).generar(datos(filas=[*VACIO, fila(part_num="SVALL2322")]))

    [error] = vista.errores
    assert (error.fila, error.columna) == (1, 1)  # fila 2 de la tabla, columna "Part_num"
    assert error.mensaje.startswith("Fila 2 › Part_num: Debe tener el formato PLCON####")


def test_precio_con_separador_de_miles_se_rechaza_en_su_celda() -> None:
    vista = VistaFalsa()

    presenter(vista).generar(datos(filas=[fila(precio_nuevo="68.083")]))

    [error] = vista.errores
    assert (error.fila, error.columna) == (0, 3)
    assert error.mensaje.startswith("Fila 1 › Precio nuevo: Debe ser un número")


def test_planes_repetidos_se_informan_como_error_general() -> None:
    vista = VistaFalsa()

    presenter(vista).generar(datos(filas=[fila(), fila()]))

    assert [e.mensaje for e in vista.errores] == [
        "Id repetido: 1208. Part_num repetido: PLCON0335."
    ]


# ---------- Flujo de generación ----------


def test_camino_feliz_escribe_la_receta_y_recuerda_autor_y_carpeta() -> None:
    vista, escritor, preferencias = VistaFalsa(), EscritorFalso(), PreferenciasEnMemoria()

    presenter(vista, escritor=escritor, preferencias=preferencias).generar(datos())

    assert vista.errores == []
    assert escritor.escrituras == [False]
    assert vista.mensajes[0].startswith("Receta generada en")
    assert preferencias.valores == {CLAVE_AUTOR: "Equipo Tecnico", CLAVE_CARPETA: "C:/recetas"}
    assert vista.trabajos == 2  # generar y escribir


def test_advertencia_senala_la_fila_de_la_tabla_y_si_cancela_no_escribe() -> None:
    vista, escritor = VistaFalsa(respuestas=False), EscritorFalso()
    generador = GeneradorFalso(advertencias=(Advertencia("PLCON0335: el precio nuevo es 0.", 1),))

    presenter(vista, generador, escritor).generar(datos(filas=[*VACIO, fila()]))

    assert vista.advertencias == ["Fila 2: PLCON0335: el precio nuevo es 0."]
    assert escritor.escrituras == []


def test_receta_existente_pide_confirmacion_y_sobrescribe() -> None:
    vista, escritor = VistaFalsa(), EscritorFalso(existe=True)

    presenter(vista, escritor=escritor).generar(datos())

    assert vista.preguntas == ["sobrescribir"]
    assert escritor.escrituras == [True]


def test_si_no_sobrescribe_no_recuerda_nada() -> None:
    vista, preferencias = VistaFalsa(respuestas=False), PreferenciasEnMemoria()

    presenter(vista, escritor=EscritorFalso(existe=True), preferencias=preferencias).generar(
        datos()
    )

    assert vista.preguntas == ["sobrescribir"]
    assert preferencias.valores == {}


def test_error_de_negocio_se_muestra_sin_romper_la_app() -> None:
    vista = VistaFalsa()

    presenter(vista, GeneradorFalso(falla=True)).generar(datos())

    assert vista.mensajes == ["ERROR: No se pudo generar el alza."]


# ---------- Importar Excel ----------


def test_importar_con_formulario_vacio_carga_sin_preguntar() -> None:
    vista = VistaFalsa()
    lector = LectorFalso([fila(), fila(id="1209", part_num="PLCON0336")])

    presenter(vista, lector=lector).importar(Path("alza.xlsx"), VACIO)

    assert vista.preguntas == []
    assert vista.cargadas is not None and len(vista.cargadas) == 2
    assert vista.mensajes[0].startswith("Se importaron 2 planes de 'alza.xlsx'")


def test_importar_sobre_datos_pide_confirmacion_y_si_cancela_no_cambia_nada() -> None:
    vista = VistaFalsa(respuestas=False)

    presenter(vista).importar(Path("alza.xlsx"), [fila()])

    assert vista.preguntas == ["reemplazar"]
    assert vista.cargadas is None


def test_excel_sin_planes_se_informa_y_no_cambia_nada() -> None:
    vista = VistaFalsa()

    presenter(vista, lector=LectorFalso([])).importar(Path("alza.xlsx"), [fila()])

    assert vista.cargadas is None
    assert vista.mensajes == ["'alza.xlsx' no trae planes. El formulario no cambió."]


def test_error_al_leer_el_excel_se_muestra() -> None:
    vista = VistaFalsa()

    presenter(vista, lector=LectorFalso(falla=True)).importar(Path("alza.xlsx"), VACIO)

    assert vista.mensajes == ["ERROR: No se pudo leer 'alza.xlsx'."]


# ---------- Limpiar formulario ----------


def test_limpiar_formulario_vacio_no_pregunta() -> None:
    vista = VistaFalsa()

    presenter(vista).limpiar(datos(filas=VACIO, requerimiento=""))

    assert vista.preguntas == []
    assert vista.limpiado


def test_limpiar_con_datos_pide_confirmacion_y_si_cancela_no_limpia() -> None:
    vista = VistaFalsa(respuestas=False)

    presenter(vista).limpiar(datos())

    assert vista.preguntas == ["limpiar"]
    assert not vista.limpiado


# ---------- Paquetes ----------


def fila_paquete(**cambios: Any) -> list[str]:
    """Una fila de la tabla con el paquete 'Paquete Datos Corporativo 4.0 Plus'."""
    paquete = datos_paquete_alza(**cambios)
    return [str(paquete[c.campo]) for c in PAQUETES.columnas]


def test_paquete_valido_llega_al_caso_de_uso_como_solicitud_de_paquetes() -> None:
    vista, generador = VistaFalsa(), GeneradorFalso()

    presenter(vista, generador, tipo=PAQUETES).generar(datos(filas=[fila_paquete()]))

    [solicitud] = generador.solicitudes
    assert isinstance(solicitud, SolicitudAlzaPaquetes)
    assert solicitud.paquetes[0].sin_iva_actual == Decimal("10605.04")


def test_paquetes_validan_su_propio_part_num() -> None:
    vista = VistaFalsa()

    presenter(vista, tipo=PAQUETES).generar(datos(filas=[fila_paquete(part_num="PLCON0335")]))

    [error] = vista.errores
    assert (error.fila, error.columna) == (0, 1)
    assert error.mensaje.startswith("Fila 1 › Part_num: Debe tener el formato SVALL####")


def test_paquetes_sin_filas_piden_al_menos_un_paquete() -> None:
    vista = VistaFalsa()

    presenter(vista, tipo=PAQUETES).generar(datos(filas=VACIO))

    assert [e.mensaje for e in vista.errores] == ["Paquetes: Debe agregar al menos un paquete."]


def test_importar_paquetes_lee_el_excel_con_los_titulos_de_paquetes() -> None:
    vista, lector = VistaFalsa(), LectorFalso([fila_paquete()])

    presenter(vista, lector=lector, tipo=PAQUETES).importar(Path("paquetes.xlsx"), VACIO)

    assert lector.formatos == [PAQUETES.formato_excel]
    assert vista.mensajes[0].startswith("Se importaron 1 paquetes de 'paquetes.xlsx'")
