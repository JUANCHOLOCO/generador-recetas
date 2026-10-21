--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753_CORRIENTE                                         | 
--|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico                                                                                  |
--|--BASE DE DATOS: PROMOTIONS                                                                                        |
--|--|--OBJETIVO DE MODIFICACIÓN: Rollback de los nuevos planes  (Fidelizacion 5.0 Plus+, Pospago 5.1 Plus+,          |
--|--|--                          Pospago 5.2 Plus+, Pospago 5.3 Plus+) a  la configuraciones de promocion            |
--|--|--AUTOR: Equipo técnico                                                                               |
--|-------------------------------------------------------------------------------------------------------------------|
set serveroutput on size 1000000
set head off
set def off
set echo on
set feed on


select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;


DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.1 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.1 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.1 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.2 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.2 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.2 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.3 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.3 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.3 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.4 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.4 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.4 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.5 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.5 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.5 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.6 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.6 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.6 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.7 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.7 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.7 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.8 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.8 FC';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.8 FC';


DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.1 FC' AND VALUE ='7751';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.2 FC' AND VALUE ='7761';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.3 FC' AND VALUE ='7771';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.4 FC' AND VALUE ='7781';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.5 FC' AND VALUE ='7791';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.6 FC' AND VALUE ='7801';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.7 FC' AND VALUE ='7811';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.8 FC' AND VALUE ='7821';


------------------------------------------------------------------------------------------------------------------------------
-- FIN SCRIPT
COMMIT;
/
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;

