--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753                                                              | 
--|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico                                                                                 |
--|--BASE DE DATOS: SIEBEL                                                                                            |
--|--OBJETIVO DE MODIFICACION: Rollback para los datos insertados en las tablas :                                     |
--|-- para la BD SIEBEL                                                                                               | 
--|-------------------------------------------------------------------------------------------------------------------|
set serveroutput on size 1000000
set head off
set def off
set echo on
set feed on



select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;
/
-- REGISTRE AQUI EL SCRIPT ESPECIFICO PARA EL ROLLBACK DEL REQUERIMIENTO : TPFB-2753- Nuevos Planes  


declare
        begin
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


               -- UPDATE add_ons_category
               UPDATE cx_add_ons_category SET cancela_cp_planes = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774]'  WHERE ID = 1;
               UPDATE cx_add_ons_category SET cancela_cp_planes = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774]'  WHERE ID = 2;
               UPDATE cx_add_ons_category SET cancela_cp_planes = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774]'  WHERE ID = 3;


        commit;
end;
-- FIN SCRIPT
/
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;

