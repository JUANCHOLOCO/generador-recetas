# Arquitectura

## 1. Objetivo y restricciones

- Aplicación de **escritorio**, un solo usuario, ejecutada en su PC sin servidor.
- **Portable**: una carpeta copiable con el ejecutable, la base de datos y la salida.
- **Extensible por módulos**: cada tipo de receta (creación de planes, alza de tarifas,
  limpieza de líneas…) se agrega sin modificar el núcleo.
- La salida debe ser **idéntica** a los instaladores que hoy produce la macro (mismo contenido,
  codificación Windows-1252, CRLF y estructura de carpetas).

## 2. Estilo arquitectónico

**Monolito modular** con **arquitectura hexagonal** (puertos y adaptadores) dentro de cada
módulo y un **registro de módulos** tipo plugin.

```
┌──────────────────────── ui (PySide6) ────────────────────────┐
│ MainWindow: menú lateral construido desde ModuleRegistry     │
└──────────────┬────────────────────┬──────────────────────────┘
               │                    │
   modules/creacion_planes_pospago  modules/<futuro módulo>
   ├── ui/            View + Presenter (MVP)
   ├── application/   casos de uso
   ├── domain/        entidades, value objects, estrategias, reglas
   ├── generators/    un generador por base de datos destino
   ├── templates/     plantillas Jinja2 de los .sql
   └── infrastructure/ modelos ORM y repositorios de parametrización
               │ depende solo de interfaces (puertos) de core
┌──────────────▼───────────────────────────────────────────────┐
│ core                                                          │
│  plugins/        contrato Module + ModuleRegistry             │
│  domain/         RecipeBundle, BillingType, errores           │
│  application/    puertos: TemplateRenderer, BundleWriter…     │
│  infrastructure/ db (SQLAlchemy), templating (Jinja2),        │
│                  files (escritor cp1252/CRLF)                 │
└───────────────────────────────────────────────────────────────┘
```

### Regla de dependencias

Las flechas apuntan siempre hacia el dominio:

`ui → application → domain` y `infrastructure → application (implementa puertos)`.

- `domain` no importa PySide6, SQLAlchemy ni Jinja2. Se prueba con tests unitarios puros.
- `core` no importa ningún módulo concreto.
- Un módulo no importa otro módulo; si comparten algo, se mueve a `core` o `shared`.

## 3. Patrones de diseño

| Patrón | Dónde | Para qué |
|---|---|---|
| Plugin / Registry | `core/plugins` | Descubrir y listar módulos sin acoplar el núcleo |
| Strategy | `BillingStrategy` (Corriente FC / Anticipada) | Encapsular lo que cambia según facturación |
| Template Method | `BaseSqlGenerator` | Estructura común aplica/rollback; cada BD implementa su cuerpo |
| Composite / Builder | `RecipeBundle` | Árbol de carpetas y archivos en memoria antes de escribir |
| Repository | `infrastructure/repositories` | El dominio pide datos sin conocer SQL |
| Use Case (Command) | `application/` | Un punto de entrada por acción de negocio |
| Value Object | `PartNum`, `Svall`, `Poid` | Validar formato una sola vez y viajar seguro |
| MVP | `ui/` de cada módulo | Lógica de pantalla testeable sin abrir ventanas |
| Factory | `billing_strategy_for(tipo)` | Elegir la estrategia desde la opción del formulario |

## 4. Flujo de generación

```
Formulario (View)
  └─► Presenter: arma SolicitudReceta (Pydantic) y la valida
        └─► Caso de uso GenerarRecetaPlanesPospago
              ├─ Factory → BillingStrategy (Corriente | Anticipada)
              ├─ Repositorios → parametrización filtrada por tipo de facturación
              ├─ Generadores ACTIVADOR, SIEBEL, PROMOTIONS, CONF → RecipeBundle
              └─ BundleWriter → carpeta de salida (cp1252, CRLF)
        └─► Presenter: muestra resultado y ofrece registrar los planes nuevos
```

## 5. Persistencia

- SQLite en un archivo `recetas.db` junto al ejecutable.
- Esquema versionado con Alembic (`src/recetas/migrations/`), aplicado automáticamente al iniciar la app.
- Cada módulo es dueño de sus tablas, con prefijo del módulo (ej. `pospago_cpl_plan_plan`).
- Los datos iniciales viven en `data/seeds/<modulo>/` y se cargan en la primera ejecución.
- Copia de seguridad automática al iniciar: `backups/recetas_YYYYMMDD_HHMMSS.db`.

## 6. Pruebas

| Tipo | Carpeta | Qué valida |
|---|---|---|
| Unitarias | `tests/unit` | Dominio, estrategias, value objects, presenters |
| Integración | `tests/integration` | Repositorios sobre SQLite temporal, escritura de archivos |
| Golden | `tests/golden` | La receta generada es idéntica byte a byte a una receta real |
| UI | `tests/unit/.../ui` con pytest-qt | Interacciones mínimas de la vista |

## 7. Cómo agregar un módulo

Ver [guia-nuevo-modulo.md](guia-nuevo-modulo.md).
