# Generador de Recetas

Aplicación de escritorio, local y portable, que genera los **instaladores SQL** (recetas) para
desplegar cambios de catálogo en las bases de datos ACTIVATOR, SIEBEL y PROMOTIONS.

Reemplaza la macro VBA del libro `Receta Planes Nintendo.xlsm`: el usuario diligencia un
formulario, la app combina esos datos con las **tablas de parametrización** (antes la hoja
"Reglas Aplicabilidad") y escribe la estructura de carpetas con los scripts `aplica-cambio` y
`rollback-cambio` de cada base de datos.

## Módulos

| Módulo | Estado | Documentación |
|---|---|---|
| Creación de planes Pospago | En construcción | [docs/modulos/creacion_planes_pospago.md](docs/modulos/creacion_planes_pospago.md) |
| Alza de tarifas | Planeado | — |
| Limpieza de líneas | Planeado | — |

## Stack

| Pieza | Tecnología |
|---|---|
| Lenguaje | Python 3.13 |
| Interfaz de escritorio | PySide6 (Qt 6), patrón MVP |
| Plantillas de los scripts | Jinja2 |
| Base de datos local | SQLite + SQLAlchemy 2 + Alembic |
| Validación de datos | Pydantic v2 |
| Pruebas | pytest, pytest-cov, pytest-qt |
| Calidad de código | ruff, mypy |
| Empaquetado portable | PyInstaller (`--onedir --windowed`) |

Las razones de cada elección están en [docs/adr/](docs/adr/).

## Estructura

```
generador-recetas/
├── docs/                 # arquitectura, ADRs, documentación por módulo, manual
├── migrations/           # migraciones Alembic del esquema SQLite
├── data/seeds/           # datos iniciales de parametrización por módulo
├── scripts/              # utilidades de desarrollo y build portable
├── output/               # recetas generadas en desarrollo (ignorado por git)
├── src/recetas/
│   ├── main.py           # punto de entrada
│   ├── config.py         # rutas (BD, output) relativas al ejecutable
│   ├── core/             # contrato de módulos, registro, puertos, adaptadores comunes
│   ├── shared/           # utilidades transversales
│   ├── ui/               # ventana principal y widgets reutilizables
│   └── modules/          # un paquete por módulo de negocio
└── tests/                # unit, integration, golden (salida byte a byte)
```

Detalle en [docs/arquitectura.md](docs/arquitectura.md).

## Desarrollo

Requisitos: Windows 10/11 y Python 3.13.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
python -m recetas
```

## Versión portable

```powershell
.\scripts\build_portable.ps1
```

Genera `dist\GeneradorRecetas\` con `GeneradorRecetas.exe`, la base `recetas.db` y la carpeta
`output\`. Se copia la carpeta completa al equipo destino; no requiere instalar Python.

## Convenciones

- Commits: [Conventional Commits](https://www.conventionalcommits.org/es/) (`feat:`, `fix:`, `test:`, `docs:`, `chore:`, `refactor:`).
- Ramas: `main` estable; una rama `feat/<fase-o-tema>` por fase.
- Cambios por versión en [CHANGELOG.md](CHANGELOG.md).
- Los scripts generados se escriben en **Windows-1252** con fin de línea CRLF, igual que los instaladores actuales.
