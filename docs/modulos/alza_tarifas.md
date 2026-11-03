# Módulo: Alza de tarifas

Genera los scripts de actualización de tarifas (aplica y rollback) en la BD **ACTIVATOR** para dos
tipos de alza: **planes pospago** y **paquetes**. Reemplaza la edición manual de los scripts.

Recetas de referencia para las pruebas golden: **TPFB-1726** (`D:\proyectosJuan\ScriptAlza`):
`pospago/` (27 planes) y `paquetes/` (283 paquetes).

**Regla principal (decisión del usuario, 2026-11-03):** el módulo **no calcula** precios. Escribe en
los scripts exactamente los valores que el usuario ingresa en el formulario o importa desde un
Excel. No hay IVA, tasas ni redondeos en la app.

Motivo: en TPFB-1726 la relación entre el precio con IVA y el precio sin IVA no es una sola tasa
(19 %, 16 %, 20 % y 23 %, y 95 paquetes con diferencias de pocos pesos), y el prorrateo de pospago
tampoco sigue una sola fórmula.

---

## 1. Tipos de alza

Un solo módulo en el menú ("Alza de tarifas") con un selector del tipo. Los dos tipos comparten la
cabecera, la estructura de carpetas y los lanzadores. Cambian las columnas de la tabla y la
plantilla SQL.

| Tipo | Tablas que actualiza |
|---|---|
| Planes pospago | `ACTIVATOR.PLANS` |
| Paquetes | `ACTIVATOR.SERVICES` y `ACTIVATOR.ATP_CORP_PRECIOS_SERVICE` |

No aplica Corriente/Anticipada.

---

## 2. Formulario

### Cabecera

| Campo | Regla |
|---|---|
| Tipo de alza | Planes pospago / Paquetes |
| Número de requerimiento | Igual que en Creación de planes (`TPFB-####`, máx. 30) |
| Autor | Igual que en Creación de planes (recordado en `preferencias.json`) |
| Ambiente | Dev / UAT / Prod: define la carpeta raíz `<RQ>_<Ambiente>` |
| Carpeta de salida | Recordada en `preferencias.json` |

### Tabla: planes pospago (una fila por plan)

| Columna | Formato | Uso |
|---|---|---|
| Id | Entero | `WHERE ID` |
| Part_num | `PLCON####` | `WHERE PART_NUM` |
| Nombre | Texto (máx. 100) | Comentario `-- Plan: <nombre>` |
| Precio nuevo | Número ≥ 0 | Aplica: `ITEM_PRICE` y `VENDOR_VALUE` |
| Prorrateo nuevo | Número ≥ 0 | Aplica: `ITEM_PRICE_PRORRATE` |
| Precio actual | Número ≥ 0 | Rollback: `ITEM_PRICE` y `VENDOR_VALUE` |
| Prorrateo actual | Número ≥ 0 | Rollback: `ITEM_PRICE_PRORRATE` |

### Tabla: paquetes (una fila por paquete)

| Columna | Formato | Uso |
|---|---|---|
| Id | Entero | `WHERE ID` en `SERVICES` |
| Part_num | `SVALL####` | `WHERE PART_NUM` en las dos tablas |
| Nombre | Texto (máx. 100) | Comentario `-- Paquete: <nombre>` |
| Precio con IVA nuevo | Número ≥ 0 | Aplica: `SERVICES.ITEM_PRICE` y `ATP_CORP_PRECIOS_SERVICE.ITEM_PRICE_IVA` |
| Precio sin IVA nuevo | Número ≥ 0 | Aplica: `ATP_CORP_PRECIOS_SERVICE.ITEM_PRICE` |
| Precio con IVA actual | Número ≥ 0 | Rollback: lo mismo que el nuevo |
| Precio sin IVA actual | Número ≥ 0 | Rollback: lo mismo que el nuevo |

`SERVICES.ITEM_PRICE` lleva siempre el precio **con IVA** (decisión del usuario, 2026-10-29). El
aplica de TPFB-1726 lo tiene mal en 265 de 283 paquetes; el golden lo declara como corrección.

### Números

- Se aceptan enteros y decimales, con punto o coma (`10605.04` o `10605,04`). Máximo 2 decimales.
- En el script van **sin comillas y con punto decimal** (`ITEM_PRICE=10605.04`), para que funcionen
  con cualquier configuración regional de Oracle.

### Importar Excel

Botón "Importar Excel" igual al de Creación de planes (importador genérico del núcleo,
`FormatoHoja`). Primera hoja, encabezados en la **fila 1** con los títulos de la tabla del tipo
elegido, datos desde la fila 2. Los planes importados reemplazan las filas (con confirmación si ya
había datos) y pasan por la misma validación.

---

## 3. Estructura de salida

```
<carpeta>/<RQ>_<Ambiente>/
└── <Carpeta del tipo>/            (AlzaPlanesPospago/ o AlzaPaquetes/)
    └── Script/
        └── ACTIVADOR/
            ├── aplica-cambio.sql
            ├── rollback-cambio.sql
            ├── SQL/1_UPDATE_<RQ>_<TIPO>_SCRIPT.SQL
            └── ROLLBACK/1_ROLLBACK_UPDATE_<RQ>_<TIPO>_SCRIPT.SQL
```

`<TIPO>` = `PLANES_POSPAGO` o `PAQUETES`. Windows-1252, CRLF, cabecera según
[estandar-scripts.md](../estandar-scripts.md). Los nombres no llevan tildes ni espacios.

Cada tipo tiene su carpeta porque el escritor reemplaza la carpeta de primer nivel: así, el alza
de planes y la de paquetes de un mismo requerimiento conviven sin borrarse.

Los `ID` y `PART_NUM` van entre comillas (`WHERE ID='1208'`), igual que en Creación de planes y en
los scripts de referencia; los precios van sin comillas.

---

## 4. Plantillas

**Aplica, planes pospago** (una pareja de líneas por plan):

```sql
-- Plan: Pospago 5.1 Empresarial
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE=68083, VENDOR_VALUE=68083, ITEM_PRICE_PRORRATE=56320 WHERE ID='1208' AND PART_NUM='PLCON0335';
```

**Aplica, paquetes** (tres líneas por paquete):

```sql
-- Paquete: Paquete Datos Corporativo 4.0 Plus
UPDATE ACTIVATOR.SERVICES SET ITEM_PRICE=13990 WHERE ID='28708' AND PART_NUM='SVALL2322';
UPDATE ACTIVATOR.ATP_CORP_PRECIOS_SERVICE SET ITEM_PRICE=11756, ITEM_PRICE_IVA=13990 WHERE PART_NUM='SVALL2322';
```

**Rollback:** las mismas sentencias con los valores **actuales**. Tiene la misma forma que el aplica:
sin el bloque `declare/begin` y sin el `/` que en TPFB-1726 vuelve a ejecutar el `select` de la hora.

Ambos terminan con `COMMIT;` y el `select` de la hora, como los scripts de referencia. Los
lanzadores (`aplica-cambio.sql`, `rollback-cambio.sql`) usan la plantilla común del núcleo con
`alter session set current_schema=ACTIVATOR;`.

---

## 5. Validaciones

**Errores (bloquean la generación):**

- Al menos una fila.
- Formato de cada columna (tabla de la sección 2); todas las columnas son obligatorias.
- No se repite el `Part_num` ni el `Id` dentro del formulario.
- Ningún texto tiene saltos de línea ni tabuladores (S1).

**Advertencias (no bloquean; el usuario decide):**

- Un precio nuevo es menor que el actual.
- Un precio nuevo es 0 (en TPFB-1726 hay 3 *Combo Mintic* en 0).
- Paquetes: el precio sin IVA es mayor que el precio con IVA.

---

## 6. Pendientes por refinar

| Tema | Situación actual |
|---|---|
| `SERVICES.ITEM_PRICE_PRORRATE` en el alza de pospago | El rollback de TPFB-1726 pospago actualiza 2 paquetes (SVALL2549 y SVALL2550), pero el aplica no trae ese script. **Fuera del alcance** por ahora: el alza de pospago solo actualiza `PLANS`. Se agrega si el usuario lo pide |
| Plantilla Excel de ejemplo | Se puede generar desde la app ("Descargar plantilla") si el usuario la pide |
