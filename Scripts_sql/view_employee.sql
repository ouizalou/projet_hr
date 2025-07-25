
use hr_sample;
-- ✅ Vue enregistrée qui affiche le nombre de départs d’employés par année
-- Utile pour mesurer le taux de rotation annuel

create or replace view annual_turnover as
select
    extract(year from departure_date) as year,
    count(*) as total_exits
from
    turnover
where
    departure_date is not null
group by
    year
order by
    year desc;

select * from annual_turnover;


-- ✅ Vue qui affiche les employés promus au cours des 12 derniers mois
-- Permet de suivre les mobilités internes récentes

create or replace view recent_promotion as
select
    e.employee_id, e.first_name,e.last_name,p.old_job_title,p.promotion_date from employees e
join promotions p on
    e.employee_id = p.employee_id
where
    p.promotion_date >= current_date - interval 12 month;

select * from recent_promotion;


-- ✅ Vue qui résume les absences par employé
-- Affiche le nombre total d'absences et le total en jours

create or replace view total_absence as
select
    a.employee_id, e.first_name,e.last_name,count(a.absence_id) as total_absence, sum(a.duration) as _total_day_absence
from absences a
 join employees e on
  a.employee_id=e.employee_id
group by
   a.employee_id,e.first_name,e.last_name;

select * from total_absence;


-- ✅ Vue qui fournit un résumé complet des départs d’employés
-- Affiche les raisons de départ et l'état administratif

create or replace view turnover_summary as
select
    t.turnover_id, 
    e.first_name,
    e.last_name ,
    t.departure_date,
    t.departure_reason,
    t.resignation_reason,
    t.statuts
from turnover t
join employees e on t.employee_id = e.employee_id;

 select * from turnover_summary;
