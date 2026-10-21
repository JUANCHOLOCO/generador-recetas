--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753                                                               | 
--|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico                                                                                  |
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


update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.1', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0446', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.1';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.1', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2616', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.1';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.1', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2624', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.1';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.2', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0447', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.2';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.2', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2617', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.2';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.2', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2625', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.2';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.3', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0448', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.3';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.3', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2618', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.3';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.3', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2626', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.3';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.4', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0449', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.4';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.4', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2619', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.4';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.4', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2627', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.4';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.5', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0450', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.5';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.5', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2620', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.5';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.5', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2628', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.5';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.6', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0451', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.6';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.6', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2621', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.6';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.6', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2629', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.6';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.7', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0452', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.7';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.7', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2622', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.7';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.7', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2630', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.7';
update siebel.s_prod_int set  DESC_TEXT = 'Pospago Conectados 5.8', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0453', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' where name = 'Pospago Conectados 5.8';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados Datos 5.8', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2623', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados Datos 5.8';
update siebel.s_prod_int set  DESC_TEXT = 'Paquete Conectados SMS 5.8', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2631', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' where name = 'Paquete Conectados SMS 5.8';


INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Pospago Conectados 5.1'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados Datos 5.1'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados SMS 5.1'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Pospago Conectados 5.2'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados Datos 5.2'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados SMS 5.2'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Pospago Conectados 5.3'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados Datos 5.3'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados SMS 5.3'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Pospago Conectados 5.4'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados Datos 5.4'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados SMS 5.4'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Pospago Conectados 5.5'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados Datos 5.5'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados SMS 5.5'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Pospago Conectados 5.6'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados Datos 5.6'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados SMS 5.6'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Pospago Conectados 5.7'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados Datos 5.7'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados SMS 5.7'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Pospago Conectados 5.8'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados Datos 5.8'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

INSERT INTO siebel.s_prod_int_x 
(
    row_id,
    Created_by,
    last_upd_by,
    par_row_id
)
SELECT
    SPI.row_id,
    SPI.Created_by,
    SPI.last_upd_by,
    SPI.row_id
FROM siebel.s_prod_int SPI
WHERE SPI.name = 'Paquete Conectados SMS 5.8'
AND NOT EXISTS (
    SELECT 1
    FROM siebel.s_prod_int_x SPX
    WHERE SPX.row_id = SPI.row_id
);

update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.1');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.1');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.1');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.2');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.2');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.2');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.3');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.3');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.3');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.4');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.4');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.4');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.5');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.5');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.5');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.6');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.6');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.6');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.7');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.7');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.7');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '120354', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.8');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.8');
update siebel.s_prod_int_x set  ATTRIB_01 = '', ATTRIB_02 = '0.0.0.1 /product 999999999 1', ATTRIB_03 = '', ATTRIB_04 = '', ATTRIB_05 = '', ATTRIB_08 = '', ATTRIB_10 = 'Y', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs', ATTRIB_50 = '', ATTRIB_45 = '0.0.0.1 /deal 999999999 0' where par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.8');


-- Sincronizacion de Poids
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000992 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990000992 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.1');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000994 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990000994 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.2');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000996 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990000996 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.3');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000998 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990000998 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.4');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001000 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001000 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.5');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001002 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001002 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.6');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001004 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001004 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.7');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001006 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/gprs',  ATTRIB_45 = '0.0.0.1 /deal 990001006 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados Datos 5.8');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000993 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990000993 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.1');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000995 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990000995 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.2');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000997 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990000997 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.3');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990000999 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990000999 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.4');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001001 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001001 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.5');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001003 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001003 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.6');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001005 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001005 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.7');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 990001007 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/sms',  ATTRIB_45 = '0.0.0.1 /deal 990001007 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Paquete Conectados SMS 5.8');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120609 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120609 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.1');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120610 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120610 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.2');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120611 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120611 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.3');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120612 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120612 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.4');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120613 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120613 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.5');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120614 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120614 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.6');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120615 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120615 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.7');
update  siebel.s_prod_int_x set  ATTRIB_02 = '0.0.0.1 /product 120616 1', ATTRIB_44 = '0.0.0.1 /service/cuentacontrol/telephony',  ATTRIB_45 = '0.0.0.1 /deal 120616 0' where   par_row_id in (select row_id from siebel.s_prod_int where name = 'Pospago Conectados 5.8');


-- UPDATE add_ons_category
UPDATE siebel.cx_add_ons_category SET cancela_cp_planes = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774][775][776][777][778][779][780][781][782]'  WHERE ID = 1;
UPDATE siebel.cx_add_ons_category SET cancela_cp_planes = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774][775][776][777][778][779][780][781][782]'  WHERE ID = 2;
UPDATE siebel.cx_add_ons_category SET cancela_cp_planes = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774][775][776][777][778][779][780][781][782]'  WHERE ID = 3;


UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2616|SVALL2624|PLCON0446|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.1';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2617|SVALL2625|PLCON0447|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.2';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2618|SVALL2626|PLCON0448|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.3';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2619|SVALL2627|PLCON0449|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.4';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2620|SVALL2628|PLCON0450|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.5';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2621|SVALL2629|PLCON0451|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.6';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2622|SVALL2630|PLCON0452|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.7';
UPDATE siebel.s_lst_of_val SET active_flg = 'Y', desc_text = 'LNALL0167|SMALL0103|PQCON0127|SVALL2623|SVALL2631|PLCON0453|', target_high = 300, target_low = 300 WHERE name = 'Pospago Conectados 5.8';


COMMIT;
-- prompt hora fin script
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;
/
