# Ajustes y mejoras pendientes

Se trabajan **después de la Fase 6B** y **antes de la Fase 7 (portable)**, junto con los ajustes que
el usuario documentó tras la primera prueba de la app.

Orden acordado (2026-10-23):

```
6A+ tema visual (terminado) → 6B parametrización → AJUSTES (estos + los del usuario)
→ 7 portable → Archivo de propiedades 5.3 → 8 segundo módulo (cuando haya un módulo real)
```

## Ajustes visuales recomendados

Ordenados por impacto para el usuario / esfuerzo. Recomendados primero: **1, 2, 3, 4 y 7**.

| # | Ajuste | Por qué | Esfuerzo | Estado |
|---|---|---|---|---|
| 1 | Botón **"Abrir carpeta"** al terminar de generar | Hoy hay que buscar la receta en el Explorador | Bajo | Pendiente |
| 2 | **Recordar la última carpeta y el autor** (`QSettings`) | No escribirlos cada vez | Bajo | Pendiente |
| 3 | **Tooltip en cada encabezado** de la tabla con el formato esperado (`PLCON####`, `SVALL####`…) | Evita errores antes de validar | Bajo | Pendiente |
| 4 | **Columnas ajustadas al contenido** y primera columna fija al desplazarse | 14 columnas no caben en pantalla | Bajo | Pendiente |
| 5 | Atajo **Ctrl+Enter** para generar y **Supr** para vaciar celdas | Más rápido con teclado | Bajo | Pendiente |
| 6 | **Barra de estado** con versión, usuario y ruta de la BD | Saber en qué app y entorno se está | Bajo | Pendiente |
| 7 | **Ícono de la aplicación** (`.ico`) para la ventana y el `.exe` | Identificación en la barra de tareas; necesario en la Fase 7 | Bajo | Pendiente |
| 8 | **Panel de resultado** dentro de la tarjeta en vez de varios `QMessageBox` seguidos | Menos ventanas emergentes; resumen de lo generado, advertencias y registro | Medio | Pendiente |
| 9 | **Validación mientras se escribe** (al salir de cada celda) | El error aparece en el momento | Medio | Pendiente |
| 10 | **Vista previa** del script antes de escribir (pestaña con el SQL) | Revisar lo que se va a desplegar | Medio | Pendiente |
| 11 | **Indicador de progreso** (cursor de espera) mientras genera | Evita el doble clic en recetas grandes | Bajo | Pendiente |
| 12 | **Fuente corporativa**, solo si marca entrega una con licencia de uso | Coherencia de marca | Bajo | Pendiente |

## Mejoras técnicas

| # | Mejora | Por qué | Esfuerzo | Estado |
|---|---|---|---|---|
| T1 | **mypy también sobre `tests/`** (`packages`/`files` en `[tool.mypy]`) | Dos errores de tests (import movido en 5B, atributo `errors`/`errores` en 6B) solo aparecieron al ejecutar; mypy los habría detectado antes | Bajo | Pendiente |

## Ajustes del usuario (primera prueba)

_Pendiente: el usuario los está documentando. Se agregan aquí al iniciar la fase de ajustes._

## Otros pendientes acordados

| Pendiente | Origen |
|---|---|
| Uso de la imagen `coloresDiseno.jpeg` en la pantalla de bienvenida | Solo si el área de comunicaciones/marca lo aprueba (docs/diseno-visual.md) |
| Login de usuario (el autor pasaría a ser el usuario logueado) | Opcional; el diseño ya lo soporta con el puerto `UsuarioActual` |
