# Diseño visual

Paleta inspirada en la pieza gráfica `coloresDiseno.jpeg` (campaña "Movistar ahora es Tigo"):
degradado diagonal verde → azul, burbujas blancas y lima, botones tipo píldora.

## Paleta

| Rol | Nombre | Hex | Uso |
|---|---|---|---|
| Degradado (inicio) | Verde | `#00C83C` | Esquina superior izquierda del fondo |
| Degradado (medio) | Verde azulado | `#0A8F8A` | Transición del fondo |
| Degradado / acción | Azul eléctrico | `#0A25D1` | Fondo, botón primario, foco, selección |
| Degradado (final) / títulos | Azul profundo | `#08137A` | Esquina inferior derecha, encabezados de tabla, títulos |
| Texto | Azul noche | `#0B1660` | Texto sobre fondos claros |
| Acento | Lima | `#D2F5A0` | Elemento seleccionado del menú, pestaña activa, filas alternas suaves |
| Superficie | Blanco | `#FFFFFF` | Tarjeta de contenido, campos, tabla |
| Error | Rojo | `#B00020` / `#F8D7DA` | Mensajes y celdas con error |

## Reglas

1. **El contenido va sobre una tarjeta blanca**, nunca directamente sobre el degradado: una tabla de
   14 columnas no es legible sobre un fondo de color.
2. **Contraste mínimo WCAG AA (4.5:1) para texto.** Sobre verde o lima el texto va en azul noche,
   nunca en blanco (blanco sobre `#00C83C` ≈ 2.4:1, insuficiente).
3. **Un solo botón primario por pantalla** (la acción principal: "Generar receta").
4. Los colores viven en un único archivo, `src/recetas/ui/resources/tema.qss`.
5. El estilo base de Qt es **Fusion**, para que la hoja de estilos se vea igual en cualquier
   versión de Windows.

## Uso de la imagen original

No se incluye la imagen como fondo: contiene una fotografía de una persona, logotipos y textos de
una campaña publicitaria. Su uso en una herramienta interna debe validarlo el área de
comunicaciones o de marca. El degradado reproduce su estética sin esos riesgos. Si se aprueba,
puede mostrarse en la pantalla de bienvenida (cuando no hay módulo seleccionado).
