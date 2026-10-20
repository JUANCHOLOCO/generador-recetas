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

### Corregido
- Scoring modelado como dos listas independientes (SCORING_PLAN y CPL_SCORING_PLAN).