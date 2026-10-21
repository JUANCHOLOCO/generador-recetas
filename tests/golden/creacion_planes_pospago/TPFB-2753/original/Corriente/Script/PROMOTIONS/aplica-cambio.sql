-----------------------------------------------
--OBJETIVO:
-- 1. Insercion de nuevo plan para modulo de promociones
--AUTOR:  Equipo Tecnico
--BASE DE DATOS: PROMOTIONS
--Cambios: - REQ-TPFB-2753_CORRIENTE
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


@SQL/1_POID_IDENTIFY_TPFB-2753_CORRIENTE.sql


EXIT
