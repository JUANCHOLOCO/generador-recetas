"""Adaptador del puerto LectorDeHojas para libros de Excel (.xlsx) con openpyxl."""

from pathlib import Path
from zipfile import BadZipFile

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from recetas.core.domain.errors import ImportacionError
from recetas.core.domain.importacion import FormatoHoja, extraer_filas


class LectorExcel:
    def leer(self, ruta: Path, formato: FormatoHoja) -> list[list[str]]:
        try:
            libro = load_workbook(ruta, read_only=True, data_only=True)
        except (InvalidFileException, BadZipFile, KeyError, OSError) as error:
            raise ImportacionError(
                f"No se pudo leer '{ruta.name}'. Use un libro de Excel .xlsx ({error})."
            ) from error
        try:
            hoja = libro.worksheets[0]
            return extraer_filas(hoja.iter_rows(values_only=True), formato)
        finally:
            libro.close()