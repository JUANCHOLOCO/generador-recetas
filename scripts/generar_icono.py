"""Genera el .ico del ejecutable a partir del ícono SVG de la app.

Uso: python scripts/generar_icono.py build/icono.ico
Lo llama scripts/build_portable.ps1; no hace falta ejecutarlo a mano.
"""

import struct
import sys
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, Qt
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer

SVG = Path(__file__).resolve().parents[1] / "src" / "recetas" / "ui" / "resources" / "icono.svg"
LADOS = (16, 24, 32, 48, 64, 128, 256)  # ventana, Explorador y barra de tareas, con y sin zoom


def png(renderer: QSvgRenderer, lado: int) -> bytes:
    imagen = QImage(lado, lado, QImage.Format.Format_ARGB32)
    imagen.fill(Qt.GlobalColor.transparent)
    pintor = QPainter(imagen)
    pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(pintor)
    pintor.end()
    datos = QByteArray()
    buffer = QBuffer(datos)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    imagen.save(buffer, "PNG")
    buffer.close()
    return datos.data()


def ico(imagenes: dict[int, bytes]) -> bytes:
    """Arma un .ico con una imagen PNG por tamaño (formato admitido desde Windows Vista)."""
    cabecera = struct.pack("<HHH", 0, 1, len(imagenes))
    posicion = len(cabecera) + 16 * len(imagenes)
    entradas = b""
    for lado, datos in imagenes.items():
        # El ancho y el alto ocupan un byte cada uno: 256 se escribe como 0.
        entradas += struct.pack(
            "<BBBBHHII", lado % 256, lado % 256, 0, 0, 1, 32, len(datos), posicion
        )
        posicion += len(datos)
    return cabecera + entradas + b"".join(imagenes.values())


def main() -> int:
    destino = Path(sys.argv[1])
    _app = QGuiApplication(sys.argv[:1])  # Qt necesita una aplicación para pintar
    renderer = QSvgRenderer(str(SVG))
    if not renderer.isValid():
        print(f"No se pudo leer {SVG}", file=sys.stderr)
        return 1
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(ico({lado: png(renderer, lado) for lado in LADOS}))
    print(f"Icono generado en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
