# Guía: agregar un módulo nuevo

Ejemplo: módulo `alza_tarifas`.

1. Crear el paquete `src/recetas/modules/alza_tarifas/` con las subcarpetas
   `domain/`, `application/`, `generators/`, `templates/sql/`, `infrastructure/` y `ui/`.
2. Crear `module.py` con una clase que implemente el contrato `Module` de `core/plugins`
   (identificador, nombre visible, widget principal y, si aplica, `initialize()` para cargar seeds).
   El constructor recibe el `AppContext` (rutas y fábrica de sesiones).
3. Registrar el módulo en `src/recetas/modules/__init__.py` (lista de módulos instalados).
4. Si el módulo necesita tablas, agregar una migración Alembic con prefijo `alza_` y sus seeds
   CSV en `src/recetas/modules/alza_tarifas/seeds/`. Importar sus modelos en `modules/models.py`.
5. Escribir las plantillas Jinja2 de los scripts y un generador por base de datos destino
   heredando de `BaseSqlGenerator`.
6. Agregar tests en `tests/unit/modules/alza_tarifas/` y al menos un caso golden en
   `tests/golden/alza_tarifas/<RQ>/`.
7. Documentar en `docs/modulos/alza_tarifas.md` (formulario, parametrización, mapeo de salida).
8. Añadir una entrada en `CHANGELOG.md`.

**Criterio de aceptación:** el módulo aparece en el menú y genera su receta **sin cambios en
`src/recetas/core/`**. Si fue necesario tocar el núcleo, documentar el motivo en un ADR.
