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
- Generador ACTIVADOR (aplica y rollback) con la regla de la matriz CPL_PLAN_PLAN documentada.
- Golden tests con parametrización real y equivalencia de sentencias con correcciones declaradas.
- Generadores SIEBEL y PROMOTIONS con plantillas de aplica y rollback.
- Equivalencia por sentencias con correcciones declaradas como funciones.
- Ambiente (Dev/UAT/Prod) en la solicitud: define la carpeta raíz `<RQ>_<Ambiente>`.
- Caso de uso `GenerarReceta` y escritor atómico de recetas en disco.
- Registro idempotente de los planes nuevos en la parametrización.
- Golden de punta a punta de la receta TPFB-2753 completa.
- Formulario de creación de planes (MVP): tabla tipo Excel con pegado, errores marcados por celda,
  advertencias, confirmación de sobrescritura y registro de planes en la parametrización.
- Tabla editable reutilizable (`ui/widgets/tabla_editable.py`).
- Tema visual (QSS) con degradado verde-azul, tarjeta de contenido, pestañas y botones píldora
  (docs/diseno-visual.md).
- Pestaña "Parametrización": mantenimiento de las 9 tablas del módulo con validación, filtro por
  tipo de facturación y guardado en una transacción.
- Mantenimiento genérico de tablas por introspección (`core`), reutilizable por cualquier módulo.
- Longitudes máximas provisionales en los campos del formulario (U3).
- Bitácora en `logs/recetas.log` y manejador global de errores inesperados (S2).
- Errores de base de datos con mensaje claro en el registro de planes y en Parametrización (S3).
- mypy revisa también los tests (T1).
- Archivos de propiedades (`Conf/*.properties`) con los planes nuevos, incluida la línea de los
  planes 5.3 en `SiebelService.properties`, para todos los ambientes.
- El nombre del plan y el código PCRF no admiten comas (separan los valores en las propiedades).

### Corregido
- Scoring modelado como dos listas independientes (SCORING_PLAN y CPL_SCORING_PLAN).
- Los códigos no numéricos de CONTROL (C01…P238) se incluyen en la parametrización.

### Cambiado
- PROMOTIONS inserta el POID real directamente y la fila PLAN_TYPE solo si no existe (decisiones B y C).
- SIEBEL usa el tarif group como POID del plan en `/product` y `/deal` (corrige el desfase de Corriente).

### Seguridad
- Los textos rechazan saltos de línea y tabuladores (formulario y parametrización), y los valores
  estáticos deben ser literales SQL válidos antes de llegar a un script (S1).