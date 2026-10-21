--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753                                                          | --|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico Accenture                                                                                  |
--|--BASE DE DATOS: ACTIVATOR                                                                                         |
--|--OBJETIVO DE MODIFICACION: Rollback para los datos insertados en las tablas :                                     |
--|--  cpl_scoring_plan, cpl_role_plan, cpl_plan_plan, vendor_profile_permission, vendor_permissions, SERVICES_PCRF   |
--|--  PLAN_SERVICE, SERVICES, PLANS, scoring_plan                                                                    |
--|-- para la BD ACTIVATOR                                                                                            | 
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
             DELETE FROM ACTIVATOR.vendor_profile_permission A WHERE A.id_permission IN ('775','776','777','778','779','780','781','782');
             DELETE FROM ACTIVATOR.vendor_permissions A WHERE A.ID IN ('775','776','777','778','779','780','781','782');
             DELETE FROM ACTIVATOR.cpl_plan_plan A WHERE A.PLAN_ID IN ('775','776','777','778','779','780','781','782') or A.PLAN_PARTNER_ID IN('775','776','777','778','779','780','781','782');
             DELETE FROM ACTIVATOR.cpl_scoring_plan A WHERE A.plan_id IN ('775','776','777','778','779','780','781','782');
             DELETE FROM ACTIVATOR.cpl_role_plan A WHERE A.plan_id IN ('775','776','777','778','779','780','781','782');
             DELETE FROM ACTIVATOR.scoring_channel A where A.id_scoring_plan IN (select id from scoring_plan where id_plan IN ('775','776','777','778','779','780','781','782'));
             DELETE FROM ACTIVATOR.scoring_plan A where A.id_plan IN ('775','776','777','778','779','780','781','782');
             DELETE FROM ACTIVATOR.plan_service A WHERE A.ID_SERVICE IN (SELECT S.ID FROM SERVICES S WHERE S.PART_NUM IN('SVALL2616','SVALL2624','SVALL2617','SVALL2625','SVALL2618','SVALL2626','SVALL2619','SVALL2627','SVALL2620','SVALL2628','SVALL2621','SVALL2629','SVALL2622','SVALL2630','SVALL2623','SVALL2631','SVALL2281','SVALL2282','SVALL2283','SVALL2284','SVALL2285','SVALL2286','SVALL2287','SVALL2288','SVALL2289','SVALL2335','SVALL2529','SVALL2615')) AND A.ID_PLAN IN ('775','776','777','778','779','780','781','782');
             DELETE FROM ACTIVATOR.services A where A.PART_NUM IN ('SVALL2616','SVALL2624','SVALL2617','SVALL2625','SVALL2618','SVALL2626','SVALL2619','SVALL2627','SVALL2620','SVALL2628','SVALL2621','SVALL2629','SVALL2622','SVALL2630','SVALL2623','SVALL2631');
             DELETE FROM ACTIVATOR.SERVICES_PCRF A WHERE A.PART_NUM IN ('SVALL2616','SVALL2624','SVALL2617','SVALL2625','SVALL2618','SVALL2626','SVALL2619','SVALL2627','SVALL2620','SVALL2628','SVALL2621','SVALL2629','SVALL2622','SVALL2630','SVALL2623','SVALL2631');
             DELETE FROM ACTIVATOR.PLANS A WHERE A.ID IN ('775','776','777','778','779','780','781','782');
        commit;
end;
-- FIN SCRIPT
/
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;
