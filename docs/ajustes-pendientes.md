# Ajustes y mejoras pendientes

Se trabajan **después de la Fase 6B** y **antes de la Fase 7 (portable)**, junto con los ajustes que
el usuario documentó tras la primera prueba de la app.

Orden acordado (actualizado 2026-10-28):

```
6A+ tema visual ✅ → 6B parametrización ✅ → Ajustes A (robustez) ✅
→ Análisis de "Alza de tarifas" → Ajustes B (uso diario) → Ajustes C (pulido)
→ 7 portable → Archivo de propiedades 5.3 → 8 módulo "Alza de tarifas"
```

| Entrega | Contenido | Estado |
|---|---|---|
| **A. Robustez y datos** | S1, U3, S2, S3, T1 | ✅ Resuelto (2026-10-28) |
| **B. Uso diario** | U1 importar Excel, U4 limpiar formulario, U2 aviso FC al elegir el tipo, visuales 1 (abrir carpeta) y 2 (recordar carpeta y autor) | Pendiente |
| **C. Pulido** | Visuales 3, 4, 5, 6, 7 y 11; D1 glosario y guía de incorporación | Pendiente |

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
| T1 | **mypy también sobre `tests/`** (`packages`/`files` en `[tool.mypy]`) | Dos errores de tests (import movido en 5B, atributo `errors`/`errores` en 6B) solo aparecieron al ejecutar; mypy los habría detectado antes | Bajo | ✅ Resuelto (entrega A) |

## Ajustes del usuario (primera prueba)

Recibidos el 2026-10-27 (el usuario puede agregar más).

| # | Ajuste | Validación | Prioridad |
|---|---|---|---|
| U1 | **Cargar los planes desde un Excel** al formulario | Viable. Los ejemplos `D:\proyectosJuan\Receta\PlanesAnticipados.xlsx` y `PlanesCorrientes.xlsx` tienen las 14 columnas en el orden del formulario (encabezado en la fila 2, datos desde la 3) y sus datos coinciden al 100 % con TPFB-2753. Requiere mover `openpyxl` de `dev` a dependencias de ejecución | Alta |
| U2 | **Aviso de "FC" al elegir Anticipada** (solo aviso) | Ya existe como advertencia al pulsar *Generar* (estrategia Anticipada, Fase 4). El ajuste es mostrarlo **en el momento** de elegir el tipo | Media |
| U3 | **Restricciones de longitud** en los campos | Hoy solo los formatos fijos (`PLCON####`, `SVALL####`) limitan la longitud; nombres, código PCRF, IDs, POIDs y tarif group no tienen máximo. Falta conocer las longitudes de las columnas Oracle de destino | ✅ Resuelto (entrega A, límites provisionales en `domain/valores.py`) |
| U4 | **Botón "Limpiar formulario"** | Viable; con confirmación si hay datos | Media |

**Decisiones del usuario (2026-10-27):**

- **U1:** el Excel debe traer al menos un plan (si viene vacío, se informa y no cambia nada). Sus planes **reemplazan** las filas del formulario, con confirmación si el formulario ya tenía datos. Lo importado pasa por la misma validación que lo escrito a mano.
- **U2:** aviso en ambos sentidos al elegir el tipo: Anticipada con nombres que terminan en `FC`, y Corriente con nombres que **no** terminan en `FC`. Solo aviso, no bloquea.
- **U3:** límites **provisionales** hasta conocer las longitudes reales de las columnas Oracle:

  | Campo | Máximo |
  |---|---|
  | Número de requerimiento | 30 |
  | Autor | 100 |
  | Nombre del producto, nombre paquete Datos y SMS | 100 |
  | Código perfil PCRF | 50 |
  | Id_Plan, Tarif group | 10 dígitos |
  | POID Datos y SMS | 20 dígitos |
  | Part_num, Svall | 9 (formato fijo, ya validado) |

## Recomendaciones de robustez y seguridad (2026-10-27)

| # | Recomendación | Por qué | Prioridad |
|---|---|---|---|
| S1 | **Rechazar caracteres de control** (saltos de línea, tabuladores) en los campos de texto | Un salto de línea dentro de un nombre partiría el literal SQL en varias líneas; en SQL*Plus una línea con solo `/` o que empiece por `@` dentro del script puede ejecutar el búfer o llamar a otro archivo | ✅ Resuelto (entrega A; además, los valores estáticos deben ser literales SQL) |
| S2 | **Manejador global de errores inesperados** con mensaje al usuario y archivo de log | Hoy un error no previsto (un bug) solo se imprime en la consola: el usuario no ve nada y no queda registro | ✅ Resuelto (entrega A, `logs/recetas.log`) |
| S3 | **Capturar errores de BD** al registrar planes y en la pestaña Parametrización (BD bloqueada, disco lleno) | Hoy solo se capturan los errores de validación; un `OperationalError` caería en el caso de S2 | ✅ Resuelto (entrega A) |
| S4 | **Fijar versiones de dependencias** (archivo de bloqueo) y revisarlas con `pip-audit` | Reproducibilidad del `.exe` y detección de vulnerabilidades conocidas. Encaja en la Fase 7 | Media (Fase 7) |
| D1 | **Glosario** (RQ, FC, POID, Svall, PLCON, Nintendo, 5.3…) y **guía de incorporación** para otro desarrollador | Facilita explicar y mantener el proyecto | Media |


## Otros pendientes acordados

| Pendiente | Origen |
|---|---|
| Uso de la imagen `coloresDiseno.jpeg` en la pantalla de bienvenida | Solo si el área de comunicaciones/marca lo aprueba (docs/diseno-visual.md) |
| Login de usuario (el autor pasaría a ser el usuario logueado) | Opcional; el diseño ya lo soporta con el puerto `UsuarioActual` |
