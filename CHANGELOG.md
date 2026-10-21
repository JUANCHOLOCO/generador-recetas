# Changelog 

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[Versionado Semántico](https://semver.org/lang/es/).

## [Sin publicar]

### Añadido
- Documentación inicial: README, arquitectura, ADR 0001–0004 y especificación del módulo
  "Creación de planes Pospago".
- Esqueleto del proyecto: ventana principal, rutas de la aplicación y configuración de pytest, ruff y mypy.
- Núcleo: contrato `Module`, `ModuleRegistry`, `RecipeBundle` (cp1252/CRLF) y `BillingType`.
- Menú lateral construido desde el registro de módulos.
- Módulo "Creación de planes Pospago" registrado (pantalla provisional).
- Persistencia SQLite con SQLAlchemy 2 y migraciones Alembic aplicadas al iniciar la app.
- Tablas de parametrización del módulo Pospago con `orden`, `tipo_facturacion` y `activo`.
- Parametrización del módulo Pospago: seeds CSV extraídos de los Excel, carga inicial idempotente
  y repositorio que filtra por tipo de facturación.
- `AppContext` y hook `Module.initialize()` para inyectar dependencias en los módulos.
- Estándar de scripts (docs/estandar-scripts.md): cp1252, CRLF, cabecera única con autor y fecha.
- Campo `autor` en la solicitud; puertos `Reloj`, `UsuarioActual` y `TemplateRenderer`.
- Plantillas Jinja2 comunes, generadores base (Template Method), wrappers de las 3 BD y Pool.
- Golden tests de aprobación + equivalencia de sentencias contra TPFB-2753.

### Corregido
- Scoring modelado como dos listas independientes (SCORING_PLAN y CPL_SCORING_PLAN).