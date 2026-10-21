--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753_CORRIENTE                                                               | 
--|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico                                                                                |
--|--BASE DE DATOS: SIEBEL                                                                                            |
--|--OBJETIVO DE MODIFICACION: Actualizar los productos                                                               |
--|-------------------------------------------------------------------------------------------------------------------|
set serveroutput on size 1000000
set head off
set def off
set echo on
set feed on


select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;
/


update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.1 FC', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0454', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.1 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.1 FC', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2632', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.1 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.1 FC', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2640', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.1 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.2 FC', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0455', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.2 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.2 FC', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2633', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.2 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.2 FC', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2641', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.2 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.3 FC', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0456', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.3 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.3 FC', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2634', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.3 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.3 FC', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2642', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.3 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.4 FC', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0457', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.4 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.4 FC', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2635', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.4 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.4 FC', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2643', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.4 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.5 FC', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0458', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.5 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.5 FC', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2636', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.5 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.5 FC', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2644', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.5 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.6 FC', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0459', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.6 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.6 FC', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2637', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.6 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.6 FC', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2645', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.6 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.7 FC', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0460', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.7 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.7 FC', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2638', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.7 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.7 FC', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2646', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.7 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.8 FC', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0461', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.8 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.8 FC', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2639', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.8 FC';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.8 FC', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2647', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.8 FC';


INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Pospago Conectados 5.1 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados Datos 5.1 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados SMS 5.1 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Pospago Conectados 5.2 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados Datos 5.2 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados SMS 5.2 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Pospago Conectados 5.3 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados Datos 5.3 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados SMS 5.3 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Pospago Conectados 5.4 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados Datos 5.4 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados SMS 5.4 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Pospago Conectados 5.5 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados Datos 5.5 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados SMS 5.5 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Pospago Conectados 5.6 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados Datos 5.6 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados SMS 5.6 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Pospago Conectados 5.7 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados Datos 5.7 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados SMS 5.7 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Pospago Conectados 5.8 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados Datos 5.8 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

INSERT INTO siebel.s_prod_int_x (row_id, Created_by, last_upd_by, par_row_id)
SELECT row_id, Created_by, last_upd_by, row_id
FROM siebel.s_prod_int
WHERE name = 'Paquete Conectados SMS 5.8 FC'
AND NOT EXISTS (
    SELECT 1 FROM siebel.s_prod_int_x x WHERE x.row_id = siebel.s_prod_int.row_id
);

update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.1 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.1 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.1 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.2 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.2 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.2 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.3 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.3 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.3 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.4 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.4 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.4 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.5 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.5 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.5 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.6 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.6 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.6 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.7 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.7 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.7 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.8 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.8 FC');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.8 FC');


-- Sincronizacion de Poids
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000885 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990000885 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.1 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001010 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001010 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.2 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001012 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001012 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.3 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001014 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001014 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.4 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001031 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001031 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.5 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001018 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001018 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.6 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001033 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001033 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.7 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001029 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001029 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.8 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001008 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001008 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.1 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001011 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001011 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.2 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001030 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001030 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.3 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001015 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001015 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.4 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001032 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001032 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.5 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001019 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001019 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.6 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001021 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001021 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.7 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001023 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001023 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.8 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120616 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120617 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.1 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120617 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120618 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.2 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120618 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120619 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.3 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120619 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120620 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.4 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120620 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120621 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.5 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120621 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120622 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.6 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120622 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120623 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.7 FC');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120623 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120624 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.8 FC');


-- UPDATE add_ons_category
UPDATE siebel.cx_add_ons_category SET cancela_cp_planes = '[7401][7411][7431][7481][7421][7451][7461][7471][7491][7501][7511][7521][7531][7541][7391][7441][7551][7561][7571][7581][7591][7601][7611][7621][7631][7641][7651][7661][7671][7681][7691][7701][7711][7721][7731][7741][7751][7761][7771][7781][7791][7801][7811][7821]'  WHERE ID = 1;
UPDATE siebel.cx_add_ons_category SET cancela_cp_planes = '[7401][7411][7431][7481][7421][7451][7461][7471][7491][7501][7511][7521][7531][7541][7391][7441][7551][7561][7571][7581][7591][7601][7611][7621][7631][7641][7651][7661][7671][7681][7691][7701][7711][7721][7731][7741][7751][7761][7771][7781][7791][7801][7811][7821]'  WHERE ID = 2;
UPDATE siebel.cx_add_ons_category SET cancela_cp_planes = '[7401][7411][7431][7481][7421][7451][7461][7471][7491][7501][7511][7521][7531][7541][7391][7441][7551][7561][7571][7581][7591][7601][7611][7621][7631][7641][7651][7661][7671][7681][7691][7701][7711][7721][7731][7741][7751][7761][7771][7781][7791][7801][7811][7821]'  WHERE ID = 3;


UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2632|SVALL2640|PLCON0454|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.1 FC';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2633|SVALL2641|PLCON0455|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.2 FC';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2634|SVALL2642|PLCON0456|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.3 FC';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2635|SVALL2643|PLCON0457|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.4 FC';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2636|SVALL2644|PLCON0458|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.5 FC';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2637|SVALL2645|PLCON0459|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.6 FC';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2638|SVALL2646|PLCON0460|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.7 FC';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2639|SVALL2647|PLCON0461|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.8 FC';

COMMIT;
-- prompt hora fin script
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;

/
