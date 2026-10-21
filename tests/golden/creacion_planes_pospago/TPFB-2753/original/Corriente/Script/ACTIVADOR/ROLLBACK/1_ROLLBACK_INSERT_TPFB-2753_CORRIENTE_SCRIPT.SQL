--|-------------------------------------------------------------------------------------------------------------------|
--|--SCRIPT # 1                                                                                                       |
--|--REQUERIMIENTO:  Creacion de nuevos planes RQ: TPFB-2753_CORRIENTE                                         | 
--|--OBJETIVO:                                                                                                        |
--|--AUTOR: Equipo tecnico                                                                                   |
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
-- REGISTRE AQUI EL SCRIPT ESPECIFICO PARA EL ROLLBACK DEL REQUERIMIENTO : TPFB-2753_CORRIENTE- Nuevos Planes  


declare
        begin
             DELETE FROM ACTIVATOR.vendor_profile_permission A WHERE A.id_permission IN ('7751','7761','7771','7781','7791','7801','7811','7821');
             DELETE FROM ACTIVATOR.vendor_permissions A WHERE A.ID IN ('7751','7761','7771','7781','7791','7801','7811','7821');
             DELETE FROM ACTIVATOR.cpl_plan_plan A WHERE A.PLAN_ID IN ('7751','7761','7771','7781','7791','7801','7811','7821') or A.PLAN_PARTNER_ID IN('7751','7761','7771','7781','7791','7801','7811','7821');
             DELETE FROM ACTIVATOR.cpl_scoring_plan A WHERE A.plan_id IN ('7751','7761','7771','7781','7791','7801','7811','7821');
             DELETE FROM ACTIVATOR.cpl_role_plan A WHERE A.plan_id IN ('7751','7761','7771','7781','7791','7801','7811','7821');
             DELETE FROM ACTIVATOR.scoring_channel A where A.id_scoring_plan IN (select id from scoring_plan where id_plan IN ('7751','7761','7771','7781','7791','7801','7811','7821'));
             DELETE FROM ACTIVATOR.scoring_plan A where A.id_plan IN ('7751','7761','7771','7781','7791','7801','7811','7821');
             DELETE FROM ACTIVATOR.plan_service A WHERE A.ID_SERVICE IN (SELECT S.ID FROM SERVICES S WHERE S.PART_NUM IN('SVALL2632','SVALL2640','SVALL2633','SVALL2641','SVALL2634','SVALL2642','SVALL2635','SVALL2643','SVALL2636','SVALL2644','SVALL2637','SVALL2645','SVALL2638','SVALL2646','SVALL2639','SVALL2647','SVALL2281','SVALL2282','SVALL2283','SVALL2284','SVALL2285','SVALL2286','SVALL2287','SVALL2288','SVALL2289','SVALL2335','SVALL2529','SVALL2615')) AND A.ID_PLAN IN ('7751','7761','7771','7781','7791','7801','7811','7821');
             DELETE FROM ACTIVATOR.services A where A.PART_NUM IN ('SVALL2632','SVALL2640','SVALL2633','SVALL2641','SVALL2634','SVALL2642','SVALL2635','SVALL2643','SVALL2636','SVALL2644','SVALL2637','SVALL2645','SVALL2638','SVALL2646','SVALL2639','SVALL2647');
             DELETE FROM ACTIVATOR.SERVICES_PCRF A WHERE A.PART_NUM IN ('SVALL2632','SVALL2640','SVALL2633','SVALL2641','SVALL2634','SVALL2642','SVALL2635','SVALL2643','SVALL2636','SVALL2644','SVALL2637','SVALL2645','SVALL2638','SVALL2646','SVALL2639','SVALL2647');
             DELETE FROM ACTIVATOR.PLANS A WHERE A.ID IN ('7751','7761','7771','7781','7791','7801','7811','7821');
        commit;
end;
-- FIN SCRIPT
/
select to_char(sysdate, 'dd/mm/yyyy hh24:mi:ss') hora, to_char (sysdate,'sssss') seg_past_midnight from dual;

