# ADR 0005: Pydantic para validar las entidades del formulario

- Estado: Aceptado
- Fecha: 2026-10-20

## Contexto

El formulario de cada módulo recibe texto desde una tabla editable (N filas × ~14 columnas). Hay
que validar formato por campo (`PLCON####`, `SVALL####`, numéricos), reglas entre campos (valor
sin IVA < con IVA) y reglas entre filas (no repetir IDs). La interfaz necesita **todos** los
errores a la vez y **la ubicación** de cada uno (fila y columna) para marcar la celda.

## Decisión

Usar **Pydantic v2** directamente en las entidades del dominio del formulario
(`PlanNuevo`, `Paquete`, `SolicitudReceta`):

- Tipos validados reutilizables con `Annotated[...]` (`PartNum`, `Svall`, `Poid`…).
- Mensajes en español con `PydanticCustomError`.
- Modelos inmutables (`frozen=True`) y sin campos desconocidos (`extra="forbid"`).
- `ValidationError.errors()` entrega la ruta de cada error, p. ej. `("planes", 2, "datos", "svall")`.

La parametrización (`Parametrizacion`) sigue siendo dataclasses: se construye desde la BD ya
validada y no necesita validación de entrada.

## Alternativas consideradas

- **Dataclasses + validación manual:** sin dependencias, pero habría que reimplementar la
  acumulación de errores con su ubicación y la conversión de texto a número.
- **DTO Pydantic en `application` + entidades puras en `domain`:** más "puro" en hexagonal, pero
  duplica cada campo en dos clases sin beneficio práctico para este proyecto.

## Consecuencias

- El dominio depende de Pydantic. Se acepta: es una librería de validación estable, sin I/O.
- Los mensajes de restricciones nativas (p. ej. texto no numérico en un entero) salen en inglés;
  la interfaz (Fase 7) los traducirá por su `type`.
- mypy usa el plugin `pydantic.mypy` para entender los constructores de los modelos.
