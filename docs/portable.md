# Versión portable

La app se entrega como una **carpeta** que se copia al equipo del usuario. No requiere instalar
Python ni permisos de administrador.

## 1. Contenido de la carpeta

```
GeneradorRecetas/
├── GeneradorRecetas.exe     ejecutable (doble clic para abrir)
├── _internal/               Python, Qt y la app empaquetados: no tocar
└── output/                  carpeta de salida propuesta por defecto
```

En el primer arranque la app crea junto al `.exe`:

| Archivo o carpeta | Qué es |
|---|---|
| `recetas.db` | Parametrización (tablas editables) y planes registrados. Se crea con los datos iniciales |
| `backups/` | Copia de `recetas.db` cada vez que se abre la app (se conservan las 10 más recientes) |
| `logs/recetas.log` | Bitácora; adjuntarla al reportar un error |
| `preferencias.json` | Último autor y carpeta de salida |

La carpeta debe estar en un lugar **con permiso de escritura** (por ejemplo, `C:\Users\<usuario>\GeneradorRecetas` o una carpeta del escritorio), no en `C:\Program Files`.

## 2. Actualizar a una versión nueva

1. Cierra la app.
2. Copia la carpeta nueva (por ejemplo, `GeneradorRecetas_0.2.0`).
3. Copia desde la carpeta vieja a la nueva: `recetas.db` y `preferencias.json`. Si quieres
   conservar el historial, también `backups/` y `logs/`.
4. Abre la versión nueva. Al iniciar, respalda la BD en `backups/` y la migra al esquema nuevo.
5. Cuando compruebes que todo funciona, borra la carpeta vieja.

Para volver atrás: cierra la app, reemplaza `recetas.db` por el respaldo de `backups/` y abre la
versión anterior.

## 3. Avisos de Windows

- **SmartScreen** ("Windows protegió su PC"): el `.exe` no está firmado digitalmente. Elegir
  *Más información → Ejecutar de todas formas*. La firma de código queda pendiente (requiere un
  certificado de la organización).
- Algunos **antivirus** marcan por error los ejecutables hechos con PyInstaller. Si pasa, reportar
  el falso positivo al área de seguridad con la ruta del `.exe`.
- No abrir **dos copias** de la app sobre la misma carpeta al mismo tiempo.

## 4. Construir la versión portable (desarrolladores)

Requisitos: Python 3.13 (`py -3.13`), conexión a internet y el entorno de desarrollo de la
[guía de incorporación](guia-incorporacion.md) activo (incluye `pip-audit`).

```powershell
.\scripts\build_portable.ps1
```

El script:

1. Revisa con `pip-audit` que ninguna versión de `requirements-build.lock` tenga
   vulnerabilidades conocidas. Si encuentra alguna, se detiene (ver "Actualizar dependencias").
2. Crea un entorno **limpio** `.venv-build` e instala exactamente las versiones del lock, más la app.
   Así el `.exe` no depende de lo que haya en el entorno de desarrollo.
3. Genera `build\icono.ico` a partir de `src/recetas/ui/resources/icono.svg`
   (`scripts/generar_icono.py`, con Qt; no requiere más librerías).
4. Ejecuta PyInstaller con `packaging/recetas.spec` (modo carpeta, sin consola).
5. Deja `dist\GeneradorRecetas\` y el comprimido `dist\GeneradorRecetas_<versión>.zip` para
   entregar. Comprime con .NET y reintenta hasta 3 veces si el antivirus tiene un archivo
   abierto (lo revisa justo después de que PyInstaller lo crea).

`-SinAuditoria` omite el paso 1. Úsalo solo sin conexión a internet y repite la auditoría antes de
entregar.

### Versiones de las dependencias

`requirements-build.lock` fija la versión **exacta** de todo lo que entra en el `.exe` (PySide6,
SQLAlchemy, Pydantic…) y de PyInstaller. Dos construcciones con el mismo lock producen la misma app.
`pyproject.toml` solo declara versiones mínimas, para el desarrollo.

**Actualizar dependencias** (a propósito, no en cada versión):

```powershell
.\scripts\actualizar_lock.ps1
git diff requirements-build.lock
pytest
.\scripts\build_portable.ps1
```

El script instala en un entorno temporal las últimas versiones que permite `pyproject.toml` y
reescribe el lock. Revisa el diff (sobre todo los saltos de versión mayor), corre las pruebas y la
lista de verificación antes de hacer commit.

### Número de versión

Una sola fuente: `__version__` en `src/recetas/__init__.py` (el `pyproject.toml` la lee de ahí).
Sigue [Versionado Semántico](https://semver.org/lang/es/):

| Cambio | Ejemplo |
|---|---|
| Corrección sin cambios visibles en la salida | 1.0.0 → 1.0.1 |
| Funcionalidad nueva o cambio compatible en los scripts | 1.0.0 → 1.1.0 |
| Cambio que obliga a cambiar la forma de trabajar o rompe recetas anteriores | 1.0.0 → 2.0.0 |

### Publicar una versión

1. Sube `__version__` y mueve las entradas de `[Sin publicar]` del CHANGELOG a una sección
   `[x.y.z] - AAAA-MM-DD`.
2. `ruff check .`, `mypy`, `pytest`.
3. `.\scripts\build_portable.ps1` y la lista de verificación de abajo.
4. Merge a `main`, etiqueta `git tag -a vx.y.z -m "Versión x.y.z"` y `git push --tags`.
5. Entrega el `.zip` con las instrucciones de la sección 2.

### Qué empaqueta la receta de PyInstaller y por qué

| Elemento | Motivo |
|---|---|
| Archivos de datos de `recetas` (`.j2`, `.qss`, `.svg`, `.csv`, `.mako`) | Plantillas, tema, ícono y seeds se leen con `importlib.resources` o `PackageLoader` |
| `recetas/migrations/**/*.py` **como archivos** | Alembic lee `env.py` y las versiones desde disco, no desde el ejecutable |
| Todos los submódulos de `recetas` y de `alembic` | `env.py` importa `recetas.modules.models`, y Alembic carga su soporte de SQLite por nombre; PyInstaller no los ve en un análisis estático |

### Lista de verificación de cada versión

Probar con el `.exe` en un equipo (o carpeta) **sin** el entorno de desarrollo:

1. Abre sin consola, con el ícono en la ventana y en la barra de tareas.
2. La barra de estado muestra la versión correcta y la ruta de `recetas.db` junto al `.exe`.
3. Se crearon `recetas.db`, `logs/recetas.log` y, al segundo arranque, un archivo en `backups/`.
4. Parametrización: las 9 tablas tienen datos.
5. Genera la receta de TPFB-2753 (importando `PlanesCorrientes.xlsx`) y el alza de paquetes de
   TPFB-1726; *Abrir carpeta* abre el Explorador.
6. Copia la carpeta a otra ruta con espacios (por ejemplo, `C:\Prueba Portable\`) y repite 1 y 5.
