use hr_sample;

alter table employees add column retirement_status enum('active','near_retirement','retired') default 'active';


-- activer le planificateur

SET GLOBAL event_scheduler = ON;

-- afficher le status scheduler

SHOW VARIABLES LIKE 'event_scheduler';

-- création d'un evenement qui permet de vérifier les employes proche de la retraite

CREATE EVENT mark_near_retirement
ON SCHEDULE EVERY 1 MONTH
DO
BEGIN
    UPDATE employees 
    SET retirement_status = 'near_retirement' 
    WHERE TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) >=37
      AND retirement_status = 'active';
END;
 

call addemployees('liza','lounas','liza_lou@gmail.com','376890546','2010-01-14',9,	6400.00,103,3);
call addemployees('taoues','lounas','taoues_lou@gmail.com','123456785','1988-03-26',9,	6400.00,103,3);

select employee_id, hire_date, TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) as service_year 
from employees where TIMESTAMPDIFF(YEAR, hire_date, CURDATE())>=37;
