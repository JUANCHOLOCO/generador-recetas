"""Adaptador del puerto Preferencias: un archivo JSON en la carpeta de la app (portable)."""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PreferenciasJson:
    def __init__(self, ruta: Path) -> None:
        self._ruta = ruta

    def leer(self, clave: str) -> str | None:
        return self._todas().get(clave)

    def guardar(self, clave: str, valor: str) -> None:
        datos = self._todas() | {clave: valor}
        try:
            self._ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            logger.warning(
                "No se pudieron guardar las preferencias en %s", self._ruta, exc_info=True
            )

    def _todas(self) -> dict[str, str]:
        try:
            datos = json.loads(self._ruta.read_text(encoding="utf-8"))
        except (OSError, ValueError):  # no existe, no se puede leer o no es JSON válido
            return {}
        if not isinstance(datos, dict):
            return {}
        return {str(clave): valor for clave, valor in datos.items() if isinstance(valor, str)}
