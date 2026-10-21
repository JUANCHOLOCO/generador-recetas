--|--------------------------------------------------------------------------|
--|--SCRIPT # 1                                                              |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753|
--|--OBJETIVO:                                                               |
--|--AUTOR: Equipo tecnico                                         |
--|--BASE DE DATOS: PROMOTIONS                                               |
--|--OBJETIVO DE MODIFICACIÓN: Agregar los nuevos planes:  ()                |
--|--|AUTOR: Equipo técnico Accenture                                        |
--|--------------------------------------------------------------------------|
set serveroutput on size 1000000
set head off
set def off
set echo on
set feed on



INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.1', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.1 telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.1', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.1 sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.1', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.1 datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.2', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.2 telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.2', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.2 sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.2', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.2 datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.3', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.3 telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.3', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.3 sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.3', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.3 datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.4', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.4 telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.4', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.4 sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.4', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.4 datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.5', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.5 telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.5', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.5 sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.5', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.5 datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.6', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.6 telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.6', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.6 sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.6', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.6 datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.7', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.7 telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.7', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.7 sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.7', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.7 datos');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Pospago Conectados 5.8', '99999', '21', 'ACTIVE', 'Descuento Pospago Conectados 5.8 telefonia');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados SMS 5.8', '99999', '22', 'ACTIVE', 'Descuento Pospago Conectados 5.8 sms');
INSERT INTO PROMOTIONS.TBL_PROM_POID_IDENTIFY (ID_PROM_POID_IDENTIFY, NAME_PACKAGE, POID, IDENTIFY, STATUS, DESCRIPTION) VALUES ((SELECT MAX(ID_PROM_POID_IDENTIFY)+1 ID_PROM_POID_IDENTIFY FROM PROMOTIONS.TBL_PROM_POID_IDENTIFY), 'Paquete Conectados Datos 5.8', '99999', '23', 'ACTIVE', 'Descuento Pospago Conectados 5.8 datos');


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
plan_name_array(0):='Pospago Conectados 5.1';
plan_name_array(1):='Pospago Conectados 5.2';
plan_name_array(2):='Pospago Conectados 5.3';
plan_name_array(3):='Pospago Conectados 5.4';
plan_name_array(4):='Pospago Conectados 5.5';
plan_name_array(5):='Pospago Conectados 5.6';
plan_name_array(6):='Pospago Conectados 5.7';
plan_name_array(7):='Pospago Conectados 5.8';


nintendo_id_plan(0):='775';
nintendo_id_plan(1):='776';
nintendo_id_plan(2):='777';
nintendo_id_plan(3):='778';
nintendo_id_plan(4):='779';
nintendo_id_plan(5):='780';
nintendo_id_plan(6):='781';
nintendo_id_plan(7):='782';


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
update promotions.tbl_prom_poid_identify set poid = '990000992' where name_package = 'Paquete Conectados Datos 5.1';
update promotions.tbl_prom_poid_identify set poid = '990000994' where name_package = 'Paquete Conectados Datos 5.2';
update promotions.tbl_prom_poid_identify set poid = '990000996' where name_package = 'Paquete Conectados Datos 5.3';
update promotions.tbl_prom_poid_identify set poid = '990000998' where name_package = 'Paquete Conectados Datos 5.4';
update promotions.tbl_prom_poid_identify set poid = '990001000' where name_package = 'Paquete Conectados Datos 5.5';
update promotions.tbl_prom_poid_identify set poid = '990001002' where name_package = 'Paquete Conectados Datos 5.6';
update promotions.tbl_prom_poid_identify set poid = '990001004' where name_package = 'Paquete Conectados Datos 5.7';
update promotions.tbl_prom_poid_identify set poid = '990001006' where name_package = 'Paquete Conectados Datos 5.8';
update promotions.tbl_prom_poid_identify set poid = '990000993' where name_package = 'Paquete Conectados SMS 5.1';
update promotions.tbl_prom_poid_identify set poid = '990000995' where name_package = 'Paquete Conectados SMS 5.2';
update promotions.tbl_prom_poid_identify set poid = '990000997' where name_package = 'Paquete Conectados SMS 5.3';
update promotions.tbl_prom_poid_identify set poid = '990000999' where name_package = 'Paquete Conectados SMS 5.4';
update promotions.tbl_prom_poid_identify set poid = '990001001' where name_package = 'Paquete Conectados SMS 5.5';
update promotions.tbl_prom_poid_identify set poid = '990001003' where name_package = 'Paquete Conectados SMS 5.6';
update promotions.tbl_prom_poid_identify set poid = '990001005' where name_package = 'Paquete Conectados SMS 5.7';
update promotions.tbl_prom_poid_identify set poid = '990001007' where name_package = 'Paquete Conectados SMS 5.8';
update promotions.tbl_prom_poid_identify set poid = '120609' where name_package = 'Pospago Conectados 5.1';
update promotions.tbl_prom_poid_identify set poid = '120610' where name_package = 'Pospago Conectados 5.2';
update promotions.tbl_prom_poid_identify set poid = '120611' where name_package = 'Pospago Conectados 5.3';
update promotions.tbl_prom_poid_identify set poid = '120612' where name_package = 'Pospago Conectados 5.4';
update promotions.tbl_prom_poid_identify set poid = '120613' where name_package = 'Pospago Conectados 5.5';
update promotions.tbl_prom_poid_identify set poid = '120614' where name_package = 'Pospago Conectados 5.6';
update promotions.tbl_prom_poid_identify set poid = '120615' where name_package = 'Pospago Conectados 5.7';
update promotions.tbl_prom_poid_identify set poid = '120616' where name_package = 'Pospago Conectados 5.8';


-- FIN SCRIPT
COMMIT;
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual; 

/
