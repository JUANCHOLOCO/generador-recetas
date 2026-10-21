# Estándar de scripts generados

Todos los módulos generan sus instaladores con este formato. La referencia funcional son los
scripts de ejemplo (p. ej. TPFB-2753); **no** se reproducen sus inconsistencias de formato, que
vienen de la macro de Excel y de ajustes manuales.

## 1. Principios

1. **Mismo efecto en BD que el ejemplo.** Las sentencias SQL son equivalentes a las del ejemplo,
   salvo las correcciones listadas en la sección 7.
2. **Mismo formato en todos los archivos.** Cabecera, bloques y espaciado idénticos sin importar
   el módulo, la base de datos o el tipo de facturación.
3. **Determinista.** La misma entrada produce exactamente los mismos bytes (la fecha se inyecta).

## 2. Formato de archivo

| Regla | Valor |
|---|---|
| Codificación | Windows-1252 (cp1252) en **todos** los archivos |
| Fin de línea | CRLF en todas las líneas, incluido un salto final |
| Espacios | Sin espacios al final de línea; sin tabuladores; un espacio entre tokens |
| Textos fijos | Solo ASCII (sin tildes: `SESION`, `Creacion`). Los datos del usuario sí pueden llevarlas |
| Nombres de archivo | Se referencian con las mismas mayúsculas/minúsculas con que se crean |

## 3. Cabecera

```
-------------------------------------------------------------------------------
-- REQUERIMIENTO : TPFB-2753_CORRIENTE
-- OBJETIVO      : Insercion de nuevos planes
-- BASE DE DATOS : ACTIVATOR
-- AUTOR         : <campo Autor del formulario / usuario logueado>
-- FECHA         : 20/10/2026
-- GENERADO POR  : Generador de Recetas 0.1.0
-------------------------------------------------------------------------------
```

## 4. Wrapper (`aplica-cambio.sql` / `rollback-cambio.sql`)

```
<cabecera>
SET HEAD OFF
SET DEF OFF
SET ECHO OFF
SET LINES 300
SET PAGES 0

WHENEVER OSERROR EXIT 9
WHENEVER SQLERROR EXIT SQL.SQLCODE

-- SE ALTERA SESION PARA EVITAR SCRIPTS NO CUALIFICADOS
ALTER SESSION SET CURRENT_SCHEMA=ACTIVATOR;

@SQL/1_INSERT_TPFB-2753_CORRIENTE_SCRIPT.SQL

EXIT
```

## 5. Script de datos (`SQL/` y `ROLLBACK/`)

```
<cabecera>
SET SERVEROUTPUT ON SIZE 1000000
SET HEAD OFF
SET DEF OFF
SET ECHO ON
SET FEED ON

SELECT TO_CHAR(SYSDATE, 'DD/MM/YYYY HH24:MI:SS') HORA_INICIO FROM DUAL;

-- ============================================================================
-- <Sección>
-- ============================================================================
<sentencias>

COMMIT;

SELECT TO_CHAR(SYSDATE, 'DD/MM/YYYY HH24:MI:SS') HORA_FIN FROM DUAL;
```

## 6. Convenciones SQL

- Palabras clave en mayúsculas (`INSERT INTO`, `VALUES`, `UPDATE`, `WHERE`).
- Tablas siempre calificadas con su esquema (`ACTIVATOR.PLANS`, `SIEBEL.S_PROD_INT_X`).
- Lista de columnas explícita en todo `INSERT` cuyo esquema se conoce.
- Literales de texto generados con el filtro `sql`: comillas simples escapadas (`'` → `''`) y
  `NULL` para valores ausentes (`None`). Nunca se concatenan valores del usuario a mano.
- `/` solo después de un bloque PL/SQL (`BEGIN ... END;`), nunca después de una sentencia que ya
  termina en `;` (en SQL*Plus la volvería a ejecutar).

## 7. Correcciones respecto a los ejemplos

| # | En el ejemplo | En el estándar |
|---|---|---|
| 1 | Wrappers en UTF-8 y scripts de datos en cp1252 | Todo en cp1252 |
| 2 | Fines de línea mezclados (CRLF y LF en el mismo archivo) | Todo CRLF |
| 3 | Cabeceras con textos distintos (`Cambios: - REQ-…` / `Cambios:  REQ -…`, "Equipo Tecnico Accenture", "SCRIPT # 1 de -") | Cabecera única (sección 3) con autor y fecha reales |
| 4 | PROMOTIONS referencia `...TPFB-2753.sql` pero el archivo es `.SQL` | Referencia exacta (falla en servidores Unix, que distinguen mayúsculas) |
| 5 | `SELECT ...;` seguido de `/` (la consulta se ejecuta dos veces) | `/` solo tras bloques PL/SQL |
| 6 | Corriente: en Siebel el `/product` del plan va desfasado en 1 respecto del tarif group | `/product` y `/deal` del plan = tarif group (como en Anticipados y en Promotions) |
| 7 | `UPDATE cx_add_ons_category` sin esquema en el rollback de Siebel | Siempre `SIEBEL.CX_ADD_ONS_CATEGORY` |

## 8. Pendientes de confirmar (cambian el comportamiento)

| # | Observación en los ejemplos | Propuesta |
|---|---|---|
| A | El rollback de SIEBEL repite los mismos `UPDATE` del aplica (no revierte nada) y deja `cancela_cp_planes` **con** los planes nuevos | Rollback que deja `cancela_cp_planes` **sin** los planes nuevos; definir qué valores restaurar en `S_PROD_INT`/`S_PROD_INT_X` |
| B | El rollback de PROMOTIONS no borra la fila `PLAN_TYPE` (`POSPAGO5`) que inserta el aplica | Borrarla también, o no insertarla si ya existe |
| C | PROMOTIONS inserta `POID = '99999'` y luego lo actualiza con el real | Insertar el POID real directamente |
| D | La carpeta raíz del ejemplo es `TPFB-2753_Prod` | Confirmar si `_Prod` es fijo, depende del ambiente o sobra |
| E | `INSERT INTO ACTIVATOR.VENDOR_PERMISSIONS VALUES (...)` sin columnas | Confirmar nombres de columnas para hacerla explícita |
| F | `last_id_table + 5` en `TBL_PROM_VARIABLES` | Confirmar por qué se deja un salto de 5 IDs |

Mientras no se confirmen, se conserva el comportamiento del ejemplo (A–F) y solo se normaliza el formato.
