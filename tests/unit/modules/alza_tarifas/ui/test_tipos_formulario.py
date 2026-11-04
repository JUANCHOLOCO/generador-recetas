from recetas.modules.alza_tarifas.domain.solicitud import (
    PaqueteAlza,
    PlanAlza,
    SolicitudAlzaPaquetes,
    SolicitudAlzaPlanes,
)
from recetas.modules.alza_tarifas.ui.tipos_formulario import PAQUETES, PLANES


def test_las_columnas_son_los_campos_de_cada_fila_en_orden() -> None:
    assert [c.campo for c in PLANES.columnas] == list(PlanAlza.model_fields)
    assert [c.campo for c in PAQUETES.columnas] == list(PaqueteAlza.model_fields)


def test_la_lista_es_el_campo_de_la_solicitud() -> None:
    assert PLANES.lista in SolicitudAlzaPlanes.model_fields
    assert PAQUETES.lista in SolicitudAlzaPaquetes.model_fields


def test_titulo_excel_e_indice_salen_de_la_configuracion() -> None:
    assert PAQUETES.titulo == "Alza de tarifas: paquetes"
    assert PAQUETES.formato_excel.encabezados[3] == "Precio con IVA nuevo"
    assert PAQUETES.indice("sin_iva_actual") == 6
    assert PAQUETES.indice("otro") is None
