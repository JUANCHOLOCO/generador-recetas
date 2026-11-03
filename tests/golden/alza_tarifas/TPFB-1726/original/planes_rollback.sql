--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Update  planes RQ: TPFB-1726_Incremento tarifario línea móvil-pospago                                                    | 
--|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico Accenture                                                                                  |
--|--BASE DE DATOS: ACTIVATOR                                                                                         |
--|--OBJETIVO DE MODIFICACION: Rollback para la actualizacion de los planes                                           |
--|-- para la BD ACTIVATOR                                                                                            | 
--|-------------------------------------------------------------------------------------------------------------------|
set serveroutput on size 1000000
set head off
set def off
set echo on
set feed on



select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;
/
-- REGISTRE AQUI EL SCRIPT ESPECIFICO PARA EL ROLLBACK DEL REQUERIMIENTO : TPFB-1726_Incremento tarifario línea móvil-pospago- Nuevos Planes  
declare
        begin
-- Plan: Pospago 5.1 Empresarial
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='61950', VENDOR_VALUE='61950', ITEM_PRICE_PRORRATE='51246,3' WHERE ID='1208' AND PART_NUM='PLCON0335';
-- Plan: Pospago 5.2 Empresarial
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='98700', VENDOR_VALUE='98700', ITEM_PRICE_PRORRATE='81646,95' WHERE ID='1209' AND PART_NUM='PLCON0336';
-- Plan: Pospago 5.3 Empresarial
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='107900', VENDOR_VALUE='107900', ITEM_PRICE_PRORRATE='89256,90' WHERE ID='1210' AND PART_NUM='PLCON0337';
-- Plan: Pospago Fidelizacion Negocios 4.9 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='42300', VENDOR_VALUE='42300', ITEM_PRICE_PRORRATE='34991,34' WHERE ID='1248' AND PART_NUM='PLCON0349';
-- Plan: Pospago Fidelizacion Negocios 5.0 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='45150', VENDOR_VALUE='45150', ITEM_PRICE_PRORRATE='37348,5' WHERE ID='1244' AND PART_NUM='PLCON0345';
-- Plan: Pospago Fidelizacion Negocios 5.01 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='52500', VENDOR_VALUE='52500', ITEM_PRICE_PRORRATE='43428' WHERE ID='1249' AND PART_NUM='PLCON0350';
-- Plan: Pospago Fidelizacion Negocios 5.21 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='68250', VENDOR_VALUE='68250', ITEM_PRICE_PRORRATE='56457,45' WHERE ID='1250' AND PART_NUM='PLCON0351';
-- Plan: Pospago Negocios 5.1 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='68250', VENDOR_VALUE='68250', ITEM_PRICE_PRORRATE='56457,45' WHERE ID='1245' AND PART_NUM='PLCON0346';
-- Plan: Pospago Negocios 5.2 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='73500', VENDOR_VALUE='73500', ITEM_PRICE_PRORRATE='60800,25' WHERE ID='1246' AND PART_NUM='PLCON0347';
-- Plan: Pospago Negocios 5.3 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='85050', VENDOR_VALUE='85050', ITEM_PRICE_PRORRATE='70355,25' WHERE ID='1247' AND PART_NUM='PLCON0348';
-- Plan: Pospago Negocios 5.4 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='52900', VENDOR_VALUE='52900', ITEM_PRICE_PRORRATE='43759,86' WHERE ID='1251' AND PART_NUM='PLCON0359';
-- Plan: Pospago Negocios 5.5 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='68700', VENDOR_VALUE='68700', ITEM_PRICE_PRORRATE='56829,91' WHERE ID='1252' AND PART_NUM='PLCON0360';
-- Plan: Pospago Negocios 5.6 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='84900', VENDOR_VALUE='84900', ITEM_PRICE_PRORRATE='70230,86' WHERE ID='1253' AND PART_NUM='PLCON0361';
-- Plan: Pospago Negocios 5.7 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='67200', VENDOR_VALUE='67200', ITEM_PRICE_PRORRATE='55590,15' WHERE ID='1255' AND PART_NUM='PLCON0372';
-- Plan: Pospago Negocios 5.8 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='77700', VENDOR_VALUE='77700', ITEM_PRICE_PRORRATE='64274,7' WHERE ID='1256' AND PART_NUM='PLCON0373';
-- Plan: Pospago Negocios 5.9 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='30975', VENDOR_VALUE='30975', ITEM_PRICE_PRORRATE='25623,15' WHERE ID='1257' AND PART_NUM='PLCON0374';
-- Plan: Pospago Negocios 5.10 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='68250', VENDOR_VALUE='68250', ITEM_PRICE_PRORRATE='57142,05' WHERE ID='1258' AND PART_NUM='PLCON0375';
-- Plan: Pospago Negocios 5.11 Plus+
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='47250', VENDOR_VALUE='47250', ITEM_PRICE_PRORRATE='39086,25' WHERE ID='1259' AND PART_NUM='PLCON0376';
-- Plan: Plan Tigo Empresarial 6.0
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='12620', VENDOR_VALUE='12620', ITEM_PRICE_PRORRATE='10605' WHERE ID='1260' AND PART_NUM='PLCON0422';
-- Plan: Plan Tigo Empresarial 6.1
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='19020', VENDOR_VALUE='19020', ITEM_PRICE_PRORRATE='15983' WHERE ID='1261' AND PART_NUM='PLCON0423';
-- Plan: Plan Tigo Empresarial 6.2
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='24320', VENDOR_VALUE='24320', ITEM_PRICE_PRORRATE='20437' WHERE ID='1262' AND PART_NUM='PLCON0424';
-- Plan: Plan Tigo Empresarial 6.3
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='31720', VENDOR_VALUE='31720', ITEM_PRICE_PRORRATE='26655' WHERE ID='1263' AND PART_NUM='PLCON0425';
-- Plan: Plan Tigo Empresarial 6.4
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='37020', VENDOR_VALUE='37020', ITEM_PRICE_PRORRATE='31109' WHERE ID='1264' AND PART_NUM='PLCON0426';
-- Plan: Plan Tigo Empresarial 6.5
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='42320', VENDOR_VALUE='42320', ITEM_PRICE_PRORRATE='35563' WHERE ID='1265' AND PART_NUM='PLCON0427';
-- Plan: Plan Tigo Empresarial 6.6
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='58120', VENDOR_VALUE='58120', ITEM_PRICE_PRORRATE='48840' WHERE ID='1266' AND PART_NUM='PLCON0428';
-- Plan: Plan Tigo Empresarial 6.7
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='69320', VENDOR_VALUE='69320', ITEM_PRICE_PRORRATE='58252' WHERE ID='1267' AND PART_NUM='PLCON0429';
-- Plan: Plan Tigo Empresarial 6.8
UPDATE ACTIVATOR.PLANS SET ITEM_PRICE='97320', VENDOR_VALUE='97320', ITEM_PRICE_PRORRATE='81545' WHERE ID='1268' AND PART_NUM='PLCON0430';
        commit;
end;
-- FIN SCRIPT
/
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;
