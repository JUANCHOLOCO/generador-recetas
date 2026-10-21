-----------------------------------------------
--OBJETIVO:
-- 1. (Procedimiento de ROLLBACK) 
--AUTOR:  Equipo Tecnico Accenture
--BASE DE DATOS: PROMOTIONS
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
alter session set current_schema=PROMOTIONS;

@ROLLBACK/1_PROMOTIONS_ROLLBACK_TPFB-2753_CORRIENTE.sql


EXIT
