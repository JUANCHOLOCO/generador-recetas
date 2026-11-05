# Guía de incorporación

Para un desarrollador que llega al proyecto. En una tarde debería poder ejecutar la app, correr
las pruebas y saber dónde tocar para un cambio típico.

## 1. Qué es y qué no es

- Una app de **escritorio, local y portable** (PySide6) que genera recetas SQL a partir de un
  formulario y de la parametrización guardada en SQLite.
- **No** se conecta a Oracle ni ejecuta los scripts: solo los escribe en una carpeta. El operador
  los despliega.
- La salida debe ser **idéntica** (byte a byte) a los instaladores que se hacían a mano o con la
  macro. Por eso hay pruebas golden y un estándar de scripts estricto.

Vocabulario del negocio: [glosario.md](glosario.md).

## 2. Orden de lectura

1. [README.md](../README.md): stack y estructura.
2. [glosario.md](glosario.md).
3. [arquitectura.md](arquitectura.md): capas, regla de dependencias y patrones.
4. [estandar-scripts.md](estandar-scripts.md): formato de todo lo que se genera.
5. La especificación del módulo que vayas a tocar, en [modulos/](modulos/).
6. [adr/](adr/): por qué Python, SQLite, plugins, PySide6 y Pydantic.
7. [ajustes-pendientes.md](ajustes-pendientes.md): qué está hecho y qué falta.

## 3. Poner el entorno

Requisitos: Windows 10/11 y Python 3.13.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m recetas
```

Al primer arranque la app crea en la raíz del repositorio `recetas.db` (aplica las migraciones y
carga los seeds), `backups/`, `logs/` y, después de generar, `preferencias.json`. Ninguno se
versiona. Para empezar de cero, cierra la app y borra `recetas.db`.

## 4. Antes de cada commit

```powershell
ruff format .
ruff check .
mypy
pytest
```

Los cuatro deben pasar. mypy corre en modo **estricto también sobre `tests/`**.

## 5. Recorrido del código

```
src/recetas/
├── main.py              composition root: crea AppContext, registra módulos y abre la ventana
├── config.py            AppPaths: rutas relativas al .exe (o a la raíz del repo en desarrollo)
├── core/                lo común a todos los módulos (no importa ningún módulo)
│   ├── domain/          RecipeBundle, BillingType, Ambiente, errores, importación de Excel
│   ├── application/     puertos (Protocol) y mantenimiento genérico de tablas
│   ├── infrastructure/  SQLite, Jinja2, escritor cp1252/CRLF, Excel, preferencias, bitácora
│   ├── plugins/         contrato Module, ModuleRegistry, AppContext
│   └── templates/sql/   plantillas comunes (cabecera, lanzadores)
├── ui/                  ventana principal, tema, manejador global de errores, widgets comunes
│   └── widgets/         TablaEditable, atajos (Ctrl+Enter), cursor de espera
└── modules/
    ├── creacion_planes_pospago/
    └── alza_tarifas/
```

Cada módulo repite la misma forma:

| Carpeta | Contiene | Depende de Qt/BD |
|---|---|---|
| `domain/` | Modelos Pydantic, value objects, validaciones, advertencias | No |
| `application/` | Casos de uso (`ejecutar`) | No |
| `generators/` + `templates/` | Un generador por BD y sus plantillas Jinja2 | No |
| `infrastructure/` | Modelos ORM, repositorios, seeds | BD |
| `ui/` | Presenter (sin Qt) + vista (Qt) | La vista |
| `module.py` | Arma todo y entrega el widget al menú | Sí |

## 6. Cómo viaja una receta

```
Vista ──datos crudos──► Presenter ──Solicitud (Pydantic)──► Caso de uso
                                                                 │
                       parametrización (repositorio) ◄───────────┤
                       generadores + plantillas ─► RecipeBundle ◄┘
Presenter ──► Escritor (disco) ──► Vista: "Receta generada en…" / Abrir carpeta
```

- Los **errores** de validación vuelven al presenter como `RecetasError` y la vista marca la celda.
- Las **advertencias** (ej. falta el sufijo FC) no bloquean: el usuario decide si sigue.
- El presenter envuelve el trabajo pesado en `vista.trabajando()` (cursor de espera), nunca los
  diálogos.

## 7. Cambios típicos

| Quiero… | Dónde |
|---|---|
| Cambiar una línea de un script generado | La plantilla `.j2` del módulo. Luego regenera los golden (sección 8) y revisa el diff |
| Agregar una validación de formato | `domain/valores.py` del módulo (value object) + test en `tests/unit/modules/<modulo>/` |
| Agregar una advertencia | `domain/advertencias.py` del módulo |
| Agregar una columna al formulario | Dominio (solicitud), `construir_solicitud` del presenter, `COLUMNAS` de la vista, `FormatoHoja` del importador de Excel, plantillas, golden y la especificación en `docs/modulos/` |
| Cambiar datos de parametrización | Desde la app (pestaña *Parametrización*). Si es un dato inicial para todos, también el CSV de `seeds/` |
| Agregar una tabla | Modelo ORM + migración Alembic con el prefijo del módulo + seeds |
| Agregar un tipo de receta nuevo | [guia-nuevo-modulo.md](guia-nuevo-modulo.md), sin tocar `core/` |
| Agregar un recurso (imagen, plantilla) | Si su extensión es nueva, añádela en `[tool.setuptools.package-data]` de `pyproject.toml` o no viajará en el paquete |

## 8. Pruebas

| Carpeta | Qué prueba | Marca |
|---|---|---|
| `tests/unit` | Dominio, generadores, presenters (con vistas falsas), widgets | `ui` en los que abren widgets |
| `tests/integration` | SQLite temporal, escritor en disco, Excel, migraciones | `integration` |
| `tests/golden` | Receta completa contra archivos aprobados y contra los scripts originales del RQ | `golden` |

**Regenerar los golden** después de un cambio intencional en la salida:

```powershell
$env:ACTUALIZAR_GOLDEN = "1"; pytest tests\golden; Remove-Item Env:ACTUALIZAR_GOLDEN
git diff tests\golden
```

Revisa el diff línea por línea antes de hacer commit: lo que quede en `esperado/` se convierte en
la verdad.

**Presenters:** se prueban con una `VistaFalsa` que guarda lo que el presenter le pide (errores,
mensajes, `trabajos`…). No abren ventanas.

## 9. Convenciones

- Código, nombres y documentación en **español**, salvo términos técnicos establecidos.
- Ramas `feat/<fase-o-tema>`; merge a `main` con `git merge --no-ff`.
- [Conventional Commits](https://www.conventionalcommits.org/es/) y una entrada en
  [CHANGELOG.md](../CHANGELOG.md) por cambio visible.
- Python 3.13 con genéricos PEP 695 (`class Presenter[S: BaseModel]`).
- Decisiones que cambian la arquitectura o tocan `core/` desde un módulo: un ADR en `docs/adr/`.

## 10. Trampas conocidas

- **Cobertura y SQLAlchemy:** medir cobertura de tests que ejecutan SQL falla con
  `InternalTraversal`. Mide cobertura solo de `tests\unit` (detalle en el README). Lo mismo puede
  pasar al depurar con breakpoints código que toca la BD.
- **Teclas en tests:** usa `QTest.keyClick` y no `qtbot.keyClick`; el segundo no tiene tipos y
  mypy estricto lo rechaza.
- **Caracteres fuera de cp1252** (emojis, flechas `→`, `≥`, el espacio invisible U+200B que llega
  al copiar desde Teams o la web) no se pueden escribir en el script. Todo texto del formulario y
  de la parametrización se valida con `caracteres_fuera_de_cp1252` (`core/domain/texto.py`); si
  agregas un campo de texto, usa los tipos de `valores.py` para heredar esa regla. Las tildes, la
  ñ, `€` y las comillas tipográficas “ ” sí existen en cp1252.
- **Saltos de línea en los datos:** se rechazan (S1). En SQL*Plus, una línea con solo `/` o que
  empiece por `@` podría ejecutar código.
- **Los originales de los RQ de referencia tienen errores** (ej. 265 precios sin IVA en el aplica
  de TPFB-1726). No los copies: decláralos como corrección en el golden.
- **El escritor reemplaza la carpeta de primer nivel**: por eso cada tipo de alza tiene su propia
  carpeta dentro de `<RQ>_<Ambiente>`.
