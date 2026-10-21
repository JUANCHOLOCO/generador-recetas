--|--------------------------------------------------------------------------|
--|--SCRIPT # 1                                                              |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753_CORRIENTE|
--|--OBJETIVO:                                                               |
--|--AUTOR: Equipo tecnico                                         |
--|--BASE DE DATOS: PROMOTIONS                                               |
--|--OBJETIVO DE MODIFICACIÓN: Agregar los nuevos planes:  ()                |
--|--|AUTOR: Equipo técnico                                        |
--|--------------------------------------------------------------------------|
set serveroutput on size 1000000
set head off
set def off
set echo on
set feed on


INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.1 FC', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.1 FC telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.1 FC', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.1 FC sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.1 FC', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.1 FC datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.2 FC', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.2 FC telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.2 FC', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.2 FC sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.2 FC', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.2 FC datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.3 FC', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.3 FC telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.3 FC', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.3 FC sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.3 FC', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.3 FC datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.4 FC', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.4 FC telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.4 FC', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.4 FC sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.4 FC', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.4 FC datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.5 FC', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.5 FC telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.5 FC', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.5 FC sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.5 FC', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.5 FC datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.6 FC', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.6 FC telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.6 FC', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.6 FC sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.6 FC', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.6 FC datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.7 FC', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.7 FC telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.7 FC', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.7 FC sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.7 FC', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.7 FC datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.8 FC', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.8 FC telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.8 FC', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.8 FC sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.8 FC', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.8 FC datos');


DECLARE
variable_type varchar2(1000);
variable_plan varchar2(1000);
last_id_table number(8);
plan_name varchar2(1000);
cancelable_plan varchar(2);


type nintendo_id_plan_type is table of varchar2(1000) index by pls_integer;
nintendo_id_plan nintendo_id_plan_type;
type plan_name_array_type is table of varchar2(1000) index by pls_integer;
plan_name_array plan_name_array_type;
BEGIN
variable_plan:='PLAN';
variable_type:='PLAN_TYPE';
plan_name:='POSPAGO5';
plan_name_array(0):='Pospago Conectados 5.1 FC';
plan_name_array(1):='Pospago Conectados 5.2 FC';
plan_name_array(2):='Pospago Conectados 5.3 FC';
plan_name_array(3):='Pospago Conectados 5.4 FC';
plan_name_array(4):='Pospago Conectados 5.5 FC';
plan_name_array(5):='Pospago Conectados 5.6 FC';
plan_name_array(6):='Pospago Conectados 5.7 FC';
plan_name_array(7):='Pospago Conectados 5.8 FC';


nintendo_id_plan(0):='7751';
nintendo_id_plan(1):='7761';
nintendo_id_plan(2):='7771';
nintendo_id_plan(3):='7781';
nintendo_id_plan(4):='7791';
nintendo_id_plan(5):='7801';
nintendo_id_plan(6):='7811';
nintendo_id_plan(7):='7821';


cancelable_plan:='NO';


dbms_output.put_line('Start insert...'||last_id_table);


dbms_output.put_line('last_id_table'||last_id_table);
SELECT max(ID_VARIABLE) INTO last_id_table FROM PROMOTIONS.tbl_prom_variables;


last_id_table:=last_id_table+5;
FOR i IN 0 .. plan_name_array.COUNT-1 LOOP
    dbms_output.put_line('insert...');
    Insert into PROMOTIONS.TBL_PROM_VARIABLES (ID_VARIABLE,VARIABLE_TYPE,NAME,VALUE,DESCRIPTION,CANCELABLE)
                values (last_id_table,variable_plan,plan_name_array(i),nintendo_id_plan(i),plan_name_array(i),cancelable_plan);
    last_id_table:=last_id_table+1;
    COMMIT;
END LOOP;


   Insert into PROMOTIONS.TBL_PROM_VARIABLES (ID_VARIABLE,VARIABLE_TYPE,NAME,VALUE,DESCRIPTION,CANCELABLE) 
                values (last_id_table,variable_type,plan_name,plan_name,plan_name,cancelable_plan);


dbms_output.put_line('insert finished...');


END;
/


-- Sincronizacion de poids 
update promotions.tbl_prom_poid_identify set poid = '990000885' where name_package = 'Paquete Conectados Datos 5.1 FC';
update promotions.tbl_prom_poid_identify set poid = '990001010' where name_package = 'Paquete Conectados Datos 5.2 FC';
update promotions.tbl_prom_poid_identify set poid = '990001012' where name_package = 'Paquete Conectados Datos 5.3 FC';
update promotions.tbl_prom_poid_identify set poid = '990001014' where name_package = 'Paquete Conectados Datos 5.4 FC';
update promotions.tbl_prom_poid_identify set poid = '990001031' where name_package = 'Paquete Conectados Datos 5.5 FC';
update promotions.tbl_prom_poid_identify set poid = '990001018' where name_package = 'Paquete Conectados Datos 5.6 FC';
update promotions.tbl_prom_poid_identify set poid = '990001033' where name_package = 'Paquete Conectados Datos 5.7 FC';
update promotions.tbl_prom_poid_identify set poid = '990001029' where name_package = 'Paquete Conectados Datos 5.8 FC';
update promotions.tbl_prom_poid_identify set poid = '990001008' where name_package = 'Paquete Conectados SMS 5.1 FC';
update promotions.tbl_prom_poid_identify set poid = '990001011' where name_package = 'Paquete Conectados SMS 5.2 FC';
update promotions.tbl_prom_poid_identify set poid = '990001030' where name_package = 'Paquete Conectados SMS 5.3 FC';
update promotions.tbl_prom_poid_identify set poid = '990001015' where name_package = 'Paquete Conectados SMS 5.4 FC';
update promotions.tbl_prom_poid_identify set poid = '990001032' where name_package = 'Paquete Conectados SMS 5.5 FC';
update promotions.tbl_prom_poid_identify set poid = '990001019' where name_package = 'Paquete Conectados SMS 5.6 FC';
update promotions.tbl_prom_poid_identify set poid = '990001021' where name_package = 'Paquete Conectados SMS 5.7 FC';
update promotions.tbl_prom_poid_identify set poid = '990001023' where name_package = 'Paquete Conectados SMS 5.8 FC';
update promotions.tbl_prom_poid_identify set poid = '120617' where name_package = 'Pospago Conectados 5.1 FC';
update promotions.tbl_prom_poid_identify set poid = '120618' where name_package = 'Pospago Conectados 5.2 FC';
update promotions.tbl_prom_poid_identify set poid = '120619' where name_package = 'Pospago Conectados 5.3 FC';
update promotions.tbl_prom_poid_identify set poid = '120620' where name_package = 'Pospago Conectados 5.4 FC';
update promotions.tbl_prom_poid_identify set poid = '120621' where name_package = 'Pospago Conectados 5.5 FC';
update promotions.tbl_prom_poid_identify set poid = '120622' where name_package = 'Pospago Conectados 5.6 FC';
update promotions.tbl_prom_poid_identify set poid = '120623' where name_package = 'Pospago Conectados 5.7 FC';
update promotions.tbl_prom_poid_identify set poid = '120624' where name_package = 'Pospago Conectados 5.8 FC';


-- FIN SCRIPT
COMMIT;
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual; 
/
