# Receta de PyInstaller para la versión portable (ver docs/portable.md).
# Uso: .\scripts\build_portable.ps1 (no ejecutar pyinstaller a mano).
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

RAIZ = Path(SPECPATH).parent
SIN_CACHE = ["**/__pycache__/*"]

# Plantillas .j2, tema .qss, ícono .svg, seeds .csv y script.py.mako de Alembic.
datas = collect_data_files("recetas", excludes=SIN_CACHE)
# Alembic lee env.py y las versiones como archivos de disco: se copian los .py tal cual.
datas += collect_data_files(
    "recetas", subdir="migrations", include_py_files=True, excludes=SIN_CACHE
)

# Lo que importan env.py y las migraciones, que PyInstaller no analiza porque son datos.
# Si una migración nueva importa algo distinto de alembic/sqlalchemy, agregarlo aquí.
hiddenimports = [
    "logging.config",
    "recetas.modules.models",
    "PySide6.QtSvg",  # plugin que dibuja el ícono SVG
]

a = Analysis(
    [str(RAIZ / "src" / "recetas" / "__main__.py")],
    pathex=[str(RAIZ / "src")],
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["tkinter"],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="GeneradorRecetas",
    icon=str(RAIZ / "build" / "icono.ico"),
    console=False,
)
coll = COLLECT(exe, a.binaries, a.datas, name="GeneradorRecetas")