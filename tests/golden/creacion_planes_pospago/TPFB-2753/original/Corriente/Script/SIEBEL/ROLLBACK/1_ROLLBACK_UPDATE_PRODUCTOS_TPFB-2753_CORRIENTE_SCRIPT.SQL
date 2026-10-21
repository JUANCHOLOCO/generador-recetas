--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753_CORRIENTE                                                              | 
--|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico                                                                               |
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
-- REGISTRE AQUI EL SCRIPT ESPECIFICO PARA EL ROLLBACK DEL REQUERIMIENTO : TPFB-2753_CORRIENTE- Nuevos Planes  


declare
        begin
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


               -- UPDATE add_ons_category
               UPDATE cx_add_ons_category SET cancela_cp_planes = '[7401][7411][7431][7481][7421][7451][7461][7471][7491][7501][7511][7521][7531][7541][7391][7441][7551][7561][7571][7581][7591][7601][7611][7621][7631][7641][7651][7661][7671][7681][7691][7701][7711][7721][7731][7741]'  WHERE ID = 1;
               UPDATE cx_add_ons_category SET cancela_cp_planes = '[7401][7411][7431][7481][7421][7451][7461][7471][7491][7501][7511][7521][7531][7541][7391][7441][7551][7561][7571][7581][7591][7601][7611][7621][7631][7641][7651][7661][7671][7681][7691][7701][7711][7721][7731][7741]'  WHERE ID = 2;
               UPDATE cx_add_ons_category SET cancela_cp_planes = '[7401][7411][7431][7481][7421][7451][7461][7471][7491][7501][7511][7521][7531][7541][7391][7441][7551][7561][7571][7581][7591][7601][7611][7621][7631][7641][7651][7661][7671][7681][7691][7701][7711][7721][7731][7741]'  WHERE ID = 3;


        commit;
end;
-- FIN SCRIPT
/
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;
