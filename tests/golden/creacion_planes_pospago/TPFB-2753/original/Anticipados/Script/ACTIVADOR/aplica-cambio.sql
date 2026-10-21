-----------------------------------------------
--OBJETIVO:
-- 1. Insercion de nuevos planes
--AUTOR:  Equipo Tecnico
--BASE DE DATOS: ACTIVATOR
--Cambios: - REQ-TPFB-2753
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

@SQL/1_INSERT_TPFB-2753_SCRIPT.SQL


EXIT
