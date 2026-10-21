-----------------------------------------------
--OBJETIVO:
-- 1. Rollback de nuevos planes
--AUTOR:  Equipo Tecnico
--BASE DE DATOS: ACTIVATOR
--Cambios:  REQ -TPFB-2753_CORRIENTE
-----------------------------------------------
SET HEAD OFF
SET DEF OFF
SET ECHO OFF
SET LINES 300
SET PAGES 0


WHENEVER OSERROR EXIT 9
WHENEVER SQLERROR EXIT SQL.SQLCODE
--SE ALTERA SESIÓN PARA EVITAR SCRIPTS NO CUALIFICADOS    
alter session set current_schema=ACTIVATOR;


@ROLLBACK/1_ROLLBACK_INSERT_TPFB-2753_CORRIENTE_SCRIPT.SQL


EXIT
