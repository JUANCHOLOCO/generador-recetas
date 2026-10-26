# Módulo: Creación de planes Pospago

Genera los instaladores SQL para crear planes Pospago (familia Nintendo) en ACTIVATOR, SIEBEL y
PROMOTIONS. Reemplaza las hojas "Consolidar Info Funcional" y "Reglas Aplicabilidad" del libro
`Receta Planes Nintendo.xlsm` y su versión Corriente `Receta Planes NintendoCorrienteV3.xlsm`.

Receta de referencia para las pruebas golden: **TPFB-2753** (carpetas `Anticipados` y `Corriente`).

---

## 1. Tipo de facturación

El formulario exige elegir uno. La lógica que cambia está en `BillingStrategy`.

| Aspecto | Anticipada | Corriente (FC) |
|---|---|---|
| `PLANS.BILLING_TYPE` | `'Anticipada'` | `'Vencida'` |
| `SERVICES.BILLING_TYPE` (Datos y SMS) | `'Vencida'` | `'Vencida'` |
| Sufijo en nombres de plan/paquete | ninguno | ` FC` (lo escribe el usuario; la app solo advierte si falta) |
| Sufijo en nombres de archivo y cabeceras | ninguno | `_CORRIENTE` |
| Carpeta de salida | `Anticipados/` | `Corriente/` |
| Matriz `CPL_PLAN_PLAN` | Nintendo + Prepago + CONTROL + ATP | Nintendo FC + Prepago |
| 5.3 OLDS | lista Anticipada | lista Corriente |
| Resto de parametrización | común (`AMBAS`) | común (`AMBAS`) |

Los IDs (ej. `775` frente a `7751`) los escribe siempre el usuario; la app no los transforma.

---

## 2. Formulario

### Cabecera

| Campo | Obligatorio | Ejemplo | Validación |
|---|---|---|---|
| Número de requerimiento | Sí | `TPFB-2753` | Texto sin espacios |
| Autor | Sí | `Juan Botero` | Precargado con el usuario de Windows (o el usuario logueado, cuando exista login) |
| Ambiente | Sí | `Prod` | `Dev`, `UAT` o `Prod`; define el sufijo de la carpeta raíz (`TPFB-2753_Prod`) |
| Carpeta de salida | Sí | `C:\receta` | Debe existir o poder crearse |
| Tipo de facturación | Sí | Corriente (FC) | `CORRIENTE` o `ANTICIPADA` |

### Tabla de planes (una fila por plan)

| Campo | Ejemplo | Validación |
|---|---|---|
| Id_Plan | `7751` | Numérico, único en el formulario |
| Part_num | `PLCON0454` | `^PLCON\d{4}$`, único |
| Nombre del producto | `Pospago Conectados 5.1 FC` | Obligatorio; si es Corriente, aviso si no termina en ` FC` |
| Valor con IVA | `19900` | Entero > 0 |
| Valor sin IVA | `16723` | Entero > 0 y menor que el valor con IVA |
| Código perfil PCRF | `Conectados_51_FC` | Obligatorio, sin espacios |
| Tarif group | `120617` | Numérico. También es el **POID del plan** |
| Es 5.3 | S/N | Por definir efecto en scripts (ver §7) |
| Nombre paquete Datos | `Paquete Conectados Datos 5.1 FC` | Obligatorio |
| Svall Datos | `SVALL2632` | `^SVALL\d{4}$`, único |
| Nombre paquete SMS | `Paquete Conectados SMS 5.1 FC` | Obligatorio |
| Svall SMS | `SVALL2640` | `^SVALL\d{4}$`, único |
| POID Datos | `990000885` | Numérico |
| POID SMS | `990001008` | Numérico |

**Orden de las columnas de la tabla** (para pegar desde Excel con Ctrl+V, en este orden exacto):

| # | Columna | # | Columna |
|---|---|---|---|
| 1 | Id_Plan | 8 | Es 5.3 (S/N) |
| 2 | Part_num | 9 | Nombre paquete Datos |
| 3 | Nombre del producto | 10 | Svall Datos |
| 4 | Valor con IVA | 11 | POID Datos |
| 5 | Valor sin IVA | 12 | Nombre paquete SMS |
| 6 | Código perfil PCRF | 13 | Svall SMS |
| 7 | Tarif group | 14 | POID SMS |

"Es 5.3" acepta `S`, `SI`, `X` (sí) o `N`, `NO`, vacío (no). Las filas completamente vacías se ignoran.

Valores que calcula la app: subtipo Datos `DPI`, subtipo SMS `SMS`, textos `0.0.0.1 /product <POID> 1`
y `0.0.0.1 /deal <POID> 0`, nombres de paquete para promociones, IDENTIFY.

---

## 3. Tablas de parametrización

Todas llevan `orden` (respeta el orden del Excel, que es el orden en que salen en los scripts),
`tipo_facturacion` (`CORRIENTE` | `ANTICIPADA` | `AMBAS`) y `activo`.
Se precargan desde `src/recetas/modules/creacion_planes_pospago/seeds/*.csv`, generados una sola vez
con `scripts/extraer_seeds_pospago.py` a partir de ambos Excel. Un dato presente en los dos libros
queda como `AMBAS`; presente solo en uno, con el tipo de ese libro.

| Tabla | Origen en Excel | Contenido | Por tipo |
|---|---|---|---|
| `pospago_cpl_plan_plan` | Cols A–D | `id_plan`, `lista` (Nintendo, Prepago, CONTROL, ATP) | **Sí** |
| `pospago_scoring` | Cols F y G | `tabla_destino` + `scoring_id`: 23 IDs para SCORING_PLAN (col F) y 24 para CPL_SCORING_PLAN (col G, incluye el 18) | No |
| `pospago_canal` | Col H | Nombres de canal para el cursor `scoring_channel` — 16 filas | No |
| `pospago_campo_estatico` | Cols J–W | `tabla`, `tipo_paquete` (PLAN/DATA/SMS), `columna`, `valor_sql`, `orden` | No* |
| `pospago_cadena_pool` | Cols Y–AB | `part_num` (`LNALL0167`, `SMALL0103`, `PQCON0127`), `orden` | No |
| `pospago_plan_53_old` | Cols AD–AE | `id_plan`, `part_num` | **Sí** |
| `pospago_identify` | Col AQ | `tipo_paquete` → IDENTIFY (PLAN=21, SMS=22, DATA=23) | No |
| `pospago_rol` | Col AS | `role_granted` (Perfil_156…) — 241 filas | No |
| `pospago_addon` | Col AU | `part_num` (SVALL2281…) — 12 filas | No |

\* `PLANS.BILLING_TYPE` no se guarda aquí: lo aporta la estrategia de facturación.

Secciones del Excel que **no** son parametrización (son datos del RQ y salen del formulario):
"Sincronización POIDs Siebel", "Sincronización POIDs Promotions" y "Configuración promociones".

### Mantenimiento desde la app

La pestaña **Parametrización** del módulo permite ver, agregar, editar, desactivar (`Activo = N`) y
eliminar filas de las 9 tablas. Reglas:

- Se guarda **toda la tabla en una transacción**: si una fila es inválida, no se guarda nada.
- El filtro por tipo de facturación solo **oculta** filas; nunca las elimina al guardar.
- `Orden` vacío = la fila va al final. `Tipo de facturación` vacío = `AMBAS`. `Activo` vacío = `S`.
- Preferir **desactivar** antes que eliminar: la fila se conserva y puede reactivarse.

### Registro de planes nuevos

Los planes del formulario se incluyen **automáticamente** en la matriz de cambios de plan del RQ
actual. Al terminar, la app pregunta si registrarlos en la parametrización:
- `pospago_cpl_plan_plan` con `lista = Nintendo` y el tipo de facturación elegido.
- `pospago_plan_53_old` si "Es 5.3 = S".

---

## 4. Estructura de salida

```
<carpeta>/<RQ>/
├── Anticipados/  (o Corriente/)
│   ├── Conf/Pool-RQ-<RQ><suf>.txt
│   └── Script/
│       ├── ACTIVADOR/
│       │   ├── aplica-cambio.sql
│       │   ├── rollback-cambio.sql
│       │   ├── SQL/1_INSERT_<RQ><suf>_SCRIPT.SQL
│       │   └── ROLLBACK/1_ROLLBACK_INSERT_<RQ><suf>_SCRIPT.SQL
│       ├── SIEBEL/
│       │   ├── aplica-cambio.sql
│       │   ├── rollback-cambio.sql
│       │   ├── SQL/1_UPDATE_PRODUCTOS_<RQ><suf>_SCRIPT.SQL
│       │   └── ROLLBACK/1_ROLLBACK_UPDATE_PRODUCTOS_<RQ><suf>_SCRIPT.SQL
│       └── PROMOTIONS/
│           ├── aplica-cambio.sql
│           ├── rollback-cambio.sql
│           ├── SQL/1_POID_IDENTIFY_<RQ><suf>.SQL
│           └── ROLLBACK/1_PROMOTIONS_ROLLBACK_<RQ><suf>.SQL
```

`<suf>` = `_CORRIENTE` para Corriente, vacío para Anticipada. Codificación Windows-1252, CRLF.

---

## 5. Mapeo campo → script

Notación: **F** = formulario, **P** = parametrización, **E** = estrategia de facturación, **C** = calculado.

### 5.1 ACTIVADOR — `1_INSERT_…_SCRIPT.SQL` (por cada plan)

| Bloque | Tabla destino | Origen de los valores |
|---|---|---|
| Plans | `ACTIVATOR.PLANS` | `ID`=F Id_Plan; `PART_NUM`=F; `NAME`, `DESCRIPTION`, `PRODUCT_DESCRIPTION`=F Nombre; `TARIFF_GROUP_ID`=F; `ITEM_PRICE`, `VENDOR_VALUE`=F Valor con IVA; `ITEM_PRICE_PRORRATE`=F Valor sin IVA; `BILLING_TYPE`=E; resto=P campos estáticos PLANS |
| Services Data | `ACTIVATOR.SERVICES` | `PART_NUM`=F Svall Datos; `PART_NUM_DESC`, `DESCRIPTION`=F Nombre paquete Datos; `PCRF_CODE`=C `MONTH/<Código PCRF>`; resto=P estáticos SERVICES DATA |
| Services SMS | `ACTIVATOR.SERVICES` | `PART_NUM`=F Svall SMS; nombres=F; resto=P estáticos SERVICES SMS |
| Plan Services DATA/SMS | `ACTIVATOR.PLAN_SERVICE` | `ID_PLAN`=F; servicio por Svall=F; resto=P estáticos PLAN_SERVICE |
| Plan Services Add Ons | `ACTIVATOR.PLAN_SERVICE` | Una fila por P add-on (`IS_DEFAULT='0'`) |
| Services PCRF | `ACTIVATOR.SERVICES_PCRF` | Svall Datos=F; `PLAN_CODE`=F Código PCRF; `PCRF_CODE`=C `MONTH/<Código PCRF>` |
| Vendor Permissions | `ACTIVATOR.VENDOR_PERMISSIONS` | `(Id_Plan, Nombre, NULL, NULL, '1')` |
| Vendor Profile Permission | `ACTIVATOR.VENDOR_PROFILE_PERMISSION` | `(0, Id_Plan)` |
| Prepago / Nintendo / ATP / Control | `ACTIVATOR.CPL_PLAN_PLAN` | Ver regla de la matriz debajo de esta tabla |
| cpl role plan | `ACTIVATOR.CPL_ROLE_PLAN` | Una fila por P rol |
| Scoring plan | `ACTIVATOR.SCORING_PLAN` | Una fila por P `id_scor` |
| cpl scoring plan | `ACTIVATOR.CPL_SCORING_PLAN` | Una fila por P `scoring_id` |

**Regla de la matriz `CPL_PLAN_PLAN`** (por cada plan nuevo `N`, en este orden; los IDs de la
parametrización que también están en el formulario se tratan como planes nuevos):

| Lista | Filas por cada ID `X` de la lista |
|---|---|
| Prepago | `(N, X)` y `(X, N)` |
| Nintendo (ya existentes) | `(X, N)` y `(N, X)` |
| Nintendo (otros planes del formulario) | solo `(X, N)`: el par inverso sale en el bloque de `X` |
| ATP | solo `(X, N)` |
| CONTROL | solo `(X, N)` (incluye los códigos C01…P238) |

TPFB-2753: Corriente 81 filas por plan (2 + 79), Anticipados 372 (2 + 79 + 24 + 267).

Al final, una sola vez: bloque PL/SQL con cursor sobre `ACTIVATOR.channel` × `scoring_plan`
filtrado por P canales y los Id_Plan del formulario → `scoring_channel`. Luego `COMMIT`.

Rollback: `DELETE` en orden inverso (vendor_profile_permission, vendor_permissions,
cpl_plan_plan, cpl_scoring_plan, cpl_role_plan, scoring_channel, scoring_plan, plan_service,
services, services_pcrf, plans) filtrando por los Id_Plan y Svall del formulario (más los Svall
de add-ons en `plan_service`).

### 5.2 SIEBEL — `1_UPDATE_PRODUCTOS_…_SCRIPT.SQL`

Por cada plan y cada paquete (Plan, Datos, SMS):

| Sentencia | Origen |
|---|---|
| `update siebel.s_prod_int set DESC_TEXT, TYPE, UOM_CD, CRT_AST_REC_FLG, PART_NUM, PROD_GLOBAL_UID, PROD_CLS_NUM where name = …` | Nombre y Part_num/Svall=F; `TYPE`: `TELEFONIA_POS` / `DATA` / `SMS`; resto=P (ver §7) |
| `insert into siebel.s_prod_int_x … where not exists …` | Nombre=F |
| `update siebel.s_prod_int_x set ATTRIB_01…ATTRIB_50 …` | `ATTRIB_02`=C `/product <POID>`; `ATTRIB_45`=C `/deal <POID>`; `ATTRIB_44`=servicio (`telephony`/`gprs`/`sms`) |
| `UPDATE siebel.s_lst_of_val SET desc_text = '<pool>|<Svall Datos>|<Svall SMS>|<Part_num>|' … where name = <Nombre plan>` | P cadena pool + F |
| `UPDATE siebel.cx_add_ons_category SET cancela_cp_planes = '[id][id]…'` | P lista Nintendo del tipo (E) + planes nuevos |

POID del plan = F Tarif group. POID de paquetes = F POID Datos / POID SMS.

### 5.3 PROMOTIONS — `1_POID_IDENTIFY_….SQL`

| Sentencia | Origen |
|---|---|
| `INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (…) VALUES ((SELECT MAX(...)+1 …), <nombre>, '99999', <IDENTIFY>, 'ACTIVE', 'Descuento <Nombre plan> <telefonia|sms|datos>')` | Por plan: 3 filas (plan, SMS, Datos); IDENTIFY=P |
| `update promotions.tbl_prom_poid_identify set poid = <POID> where name_package = …` | F POIDs |
| Bloque PL/SQL `TBL_PROM_VARIABLES` | Arreglos con Nombre e Id_Plan del formulario |

Rollback: `DELETE` por `NAME_PACKAGE` en `TBL_PROM_POID_IDENTIFY` y por `NAME`/`VALUE` en `TBL_PROM_VARIABLES`.

### 5.4 Conf — `Pool-RQ-<RQ><suf>.txt`

Un nombre de plan por línea, en el orden del formulario.

---

## 6. Validaciones de negocio

**Errores (bloquean la generación).** Implementados con Pydantic en `domain/plan.py`:

- Formato de cada campo según la tabla de la sección 2 (`PLCON####`, `SVALL####`, IDs y POIDs numéricos).
- Valor sin IVA menor que el valor con IVA.
- Al menos un plan.
- No se repiten Id_Plan, Part_num ni Svall (de Datos y SMS juntos) dentro del formulario.

**Advertencias (no bloquean; el usuario decide).** Implementadas en `domain/advertencias.py`:

- Un Id_Plan del formulario ya existe en la matriz de cambios de plan del mismo tipo.
- No hay planes Nintendo configurados para el tipo de facturación elegido.
- Corriente: un nombre de plan o paquete no termina en ` FC`.
- Anticipada: un nombre de plan o paquete termina en ` FC` (posible tipo de facturación equivocado).

---

## 7. Pendientes por refinar

| Tema | Situación actual |
|---|---|
| Efecto de "Es 5.3 = S" | Genera un **archivo de propiedades**. Se implementará en una entrega posterior, cuando la generación de scripts de BD funcione. Por ahora el campo solo se captura y se usa para registrar el plan en 5.3 OLDS |
| Valores fijos en Siebel: `PROD_GLOBAL_UID='11042'`, `PROD_CLS_NUM='120'`, `UOM_CD='Por mes'`, `ATTRIB_04='120354'`, `target_high/low=300`, IDs `1,2,3` de `cx_add_ons_category` | Se tratarán como campos estáticos de parametrización; confirmar que no varían por plan |
| Bloque `TBL_PROM_VARIABLES` (`plan_name='POSPAGO5'`, `cancelable_plan='NO'`) | Confirmar si son fijos o dependen del RQ |
| "Es Retención" | Excluido del formulario por decisión del usuario |
| `PLAN_TYPE` de PROMOTIONS (`POSPAGO5`) y valores fijos de SIEBEL (`11042`, `120`, `120354`, `Por mes`, IDs `1,2,3` de `CX_ADD_ONS_CATEGORY`, `300`) | **Resuelto (2026-10-22):** el usuario confirmó que son constantes de la familia Pospago. Quedan como constantes con nombre en los generadores. Si un módulo futuro maneja otra familia, se parametrizan |
| Códigos no numéricos en la columna CONTROL (C01…C25, P02…P238) | **Resuelto:** el script de Anticipados sí los usa (267 filas de CONTROL por plan). Se cargan en la parametrización como cualquier otro ID |
