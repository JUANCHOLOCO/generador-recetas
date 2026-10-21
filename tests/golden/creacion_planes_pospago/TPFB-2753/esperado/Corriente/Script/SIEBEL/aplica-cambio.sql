-------------------------------------------------------------------------------
-- REQUERIMIENTO : TPFB-2753_CORRIENTE
-- OBJETIVO      : Actualizacion de los productos de los nuevos planes
-- BASE DE DATOS : SIEBEL
-- AUTOR         : Equipo Tecnico
-- FECHA         : 20/10/2026
-- GENERADO POR  : Generador de Recetas 0.1.0
-------------------------------------------------------------------------------
SET HEAD OFF
SET DEF OFF
SET ECHO OFF
SET LINES 300
SET PAGES 0

WHENEVER OSERROR EXIT 9
WHENEVER SQLERROR EXIT SQL.SQLCODE

-- SE ALTERA SESION PARA EVITAR SCRIPTS NO CUALIFICADOS
ALTER SESSION SET CURRENT_SCHEMA=SIEBEL;

@SQL/1_UPDATE_PRODUCTOS_TPFB-2753_CORRIENTE_SCRIPT.SQL

EXIT
