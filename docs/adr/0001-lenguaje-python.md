# ADR 0001: Python 3.13 como lenguaje

- Estado: Aceptado
- Fecha: 2026-10-19

## Contexto

Se necesita reemplazar una macro VBA que genera scripts SQL a partir de un formulario y de
tablas de reglas. El trabajo es mayoritariamente generación de texto con plantillas, validación
de datos y lectura de una base local. La app debe ser portable en Windows y mantenible por una
persona que está aprendiendo.

## Decisión

Usar **Python 3.13** (ya instalado en el equipo del usuario).

## Alternativas consideradas

- **C# / .NET (WinForms o WPF):** ejecutable nativo y muy buen soporte en Windows, pero más
  código para formularios dinámicos y plantillas; curva de aprendizaje mayor.
- **Seguir con VBA:** sin pruebas automatizadas, difícil de versionar y de extender por módulos.
- **Java:** requiere JRE o empaquetado pesado; no aporta ventajas para este caso.

## Consecuencias

- Ecosistema maduro para plantillas (Jinja2), ORM (SQLAlchemy), validación (Pydantic) y pruebas (pytest).
- El ejecutable portable se genera con PyInstaller (carpeta de ~100–150 MB con Qt incluido).
- Se usarán *type hints* y mypy para compensar la tipificación dinámica.
