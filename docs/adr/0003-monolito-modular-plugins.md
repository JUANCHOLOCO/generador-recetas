# ADR 0003: Monolito modular, hexagonal y registro de módulos

- Estado: Aceptado
- Fecha: 2026-10-19

## Contexto

Hoy existe un tipo de receta (creación de planes Pospago) y se esperan otros: alza de tarifas,
limpieza de líneas, etc. Cada uno tendrá formulario, parametrización, plantillas y salida propios,
pero compartirán infraestructura (BD, plantillas, escritura de archivos, ventana principal).

## Decisión

- Un solo ejecutable (**monolito modular**), con un paquete por módulo en `src/recetas/modules/`.
- Dentro de cada módulo, **arquitectura hexagonal**: `domain` y `application` dependen solo de
  interfaces (puertos); `infrastructure` y `ui` son adaptadores.
- Contrato `Module` + `ModuleRegistry` en `core/plugins`. La ventana principal construye su menú
  a partir del registro.

## Alternativas consideradas

- **Una app por tipo de receta:** duplicación de infraestructura y varias apps que mantener.
- **Capas planas sin módulos (models/, views/, services/):** con varios módulos se mezclan las
  responsabilidades y crece el acoplamiento.
- **Plugins externos con entry points de paquetes:** más flexible pero innecesario mientras todos
  los módulos vivan en el mismo repositorio.

## Consecuencias

- Agregar un módulo no requiere tocar `core/` (criterio verificable).
- Más carpetas y archivos al inicio; se compensa con límites claros y tests aislados.
