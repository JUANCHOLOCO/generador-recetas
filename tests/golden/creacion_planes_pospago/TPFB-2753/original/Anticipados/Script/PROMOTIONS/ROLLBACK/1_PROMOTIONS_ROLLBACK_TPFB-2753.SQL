--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753                                         | 
--|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico Accenture                                                                                  |
--|--BASE DE DATOS: PROMOTIONS                                                                                        |
--|--|--OBJETIVO DE MODIFICACIÓN: Rollback de los nuevos planes  (Fidelizacion 5.0 Plus+, Pospago 5.1 Plus+,          |
--|--|--                          Pospago 5.2 Plus+, Pospago 5.3 Plus+) a  la configuraciones de promocion            |
--|--|--AUTOR: Equipo técnico Accenture                                                                               |
--|-------------------------------------------------------------------------------------------------------------------|
set serveroutput on size 1000000
set head off
set def off
set echo on
set feed on



select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;


DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.1';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.1';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.1';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.2';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.2';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.2';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.3';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.3';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.3';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.4';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.4';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.4';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.5';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.5';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.5';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.6';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.6';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.6';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.7';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.7';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.7';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Pospago Conectados 5.8';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados SMS 5.8';
DELETE FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY WHERE NAME_PACKAGE = 'Paquete Conectados Datos 5.8';


DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.1' AND VALUE ='775';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.2' AND VALUE ='776';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.3' AND VALUE ='777';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.4' AND VALUE ='778';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.5' AND VALUE ='779';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.6' AND VALUE ='780';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.7' AND VALUE ='781';
DELETE FROM PROMOTIONS.TBL_PROM_VARIABLES WHERE NAME='Pospago Conectados 5.8' AND VALUE ='782';


------------------------------------------------------------------------------------------------------------------------------
-- FIN SCRIPT
COMMIT;
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;
/
