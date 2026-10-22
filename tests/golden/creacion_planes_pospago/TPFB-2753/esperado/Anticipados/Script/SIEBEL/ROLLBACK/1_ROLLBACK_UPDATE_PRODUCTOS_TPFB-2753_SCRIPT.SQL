-------------------------------------------------------------------------------
-- REQUERIMIENTO : TPFB-2753
-- OBJETIVO      : Rollback de la actualizacion de los productos
-- BASE DE DATOS : SIEBEL
-- AUTOR         : Equipo Tecnico
-- FECHA         : 20/10/2026
-- GENERADO POR  : Generador de Recetas 0.1.0
-------------------------------------------------------------------------------
SET SERVEROUTPUT ON SIZE 1000000
SET HEAD OFF
SET DEF OFF
SET ECHO ON
SET FEED ON

SELECT TO_CHAR(SYSDATE, 'DD/MM/YYYY HH24:MI:SS') HORA_INICIO FROM DUAL;

-- ============================================================================
-- Rollback de los productos (los UPDATE se repiten: decision A)
-- ============================================================================
DECLARE
BEGIN
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Pospago Conectados 5.1', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0446', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' WHERE NAME = 'Pospago Conectados 5.1';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados Datos 5.1', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2616', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados Datos 5.1';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados SMS 5.1', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2624', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados SMS 5.1';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Pospago Conectados 5.2', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0447', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' WHERE NAME = 'Pospago Conectados 5.2';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados Datos 5.2', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2617', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados Datos 5.2';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados SMS 5.2', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2625', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados SMS 5.2';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Pospago Conectados 5.3', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0448', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' WHERE NAME = 'Pospago Conectados 5.3';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados Datos 5.3', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2618', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados Datos 5.3';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados SMS 5.3', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2626', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados SMS 5.3';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Pospago Conectados 5.4', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0449', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' WHERE NAME = 'Pospago Conectados 5.4';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados Datos 5.4', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2619', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados Datos 5.4';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados SMS 5.4', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2627', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados SMS 5.4';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Pospago Conectados 5.5', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0450', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' WHERE NAME = 'Pospago Conectados 5.5';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados Datos 5.5', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2620', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados Datos 5.5';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados SMS 5.5', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2628', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados SMS 5.5';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Pospago Conectados 5.6', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0451', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' WHERE NAME = 'Pospago Conectados 5.6';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados Datos 5.6', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2621', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados Datos 5.6';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados SMS 5.6', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2629', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados SMS 5.6';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Pospago Conectados 5.7', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0452', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' WHERE NAME = 'Pospago Conectados 5.7';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados Datos 5.7', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2622', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados Datos 5.7';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados SMS 5.7', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2630', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados SMS 5.7';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Pospago Conectados 5.8', TYPE = 'TELEFONIA_POS', UOM_CD = 'Por mes', CRT_AST_REC_FLG = 'Y', PART_NUM = 'PLCON0453', PROD_GLOBAL_UID = '11042', PROD_CLS_NUM = '120' WHERE NAME = 'Pospago Conectados 5.8';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados Datos 5.8', TYPE = 'DATA', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2623', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados Datos 5.8';
  UPDATE SIEBEL.S_PROD_INT SET DESC_TEXT = 'Paquete Conectados SMS 5.8', TYPE = 'SMS', UOM_CD = '', CRT_AST_REC_FLG = 'Y', PART_NUM = 'SVALL2631', PROD_GLOBAL_UID = '', PROD_CLS_NUM = '' WHERE NAME = 'Paquete Conectados SMS 5.8';
  UPDATE SIEBEL.CX_ADD_ONS_CATEGORY SET CANCELA_CP_PLANES = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774]' WHERE ID = 1;
  UPDATE SIEBEL.CX_ADD_ONS_CATEGORY SET CANCELA_CP_PLANES = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774]' WHERE ID = 2;
  UPDATE SIEBEL.CX_ADD_ONS_CATEGORY SET CANCELA_CP_PLANES = '[739][740][741][742][743][744][745][746][747][748][749][750][751][752][753][754][755][756][757][758][759][760][761][762][763][764][765][766][767][768][769][770][771][772][773][774]' WHERE ID = 3;

  COMMIT;
END;
/

COMMIT;

SELECT TO_CHAR(SYSDATE, 'DD/MM/YYYY HH24:MI:SS') HORA_FIN FROM DUAL;