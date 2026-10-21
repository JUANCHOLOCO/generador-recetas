-----------------------------------------------
--OBJETIVO:
-- 1. Rollback update de los nuevos Planes
--AUTOR:  Equipo Tecnico
--BASE DE DATOS: SIEBEL
--Cambios:  REQ -TPFB-2753
-----------------------------------------------
SET HEAD OFF
SET DEF OFF
SET ECHO OFF
SET LINES 300
SET PAGES 0


WHENEVER OSERROR EXIT 9
WHENEVER SQLERROR EXIT SQL.SQLCODE

--SE ALTERA SESIÓN PARA EVITAR SCRIPTS NO CUALIFICADOS    
alter session set current_schema=SIEBEL;

@ROLLBACK/1_ROLLBACK_UPDATE_PRODUCTOS_TPFB-2753_SCRIPT.SQL


EXIT
