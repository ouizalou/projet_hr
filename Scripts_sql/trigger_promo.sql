
use hr_sample;

# creation d'un declencheur qui permet d'empecher l'insertion d'un employe dans la table promotion 
# si le id_employee fourni n'existe pas, il declenche un messge d'erreur

CREATE TRIGGER before_promotion_insert
BEFORE insert ON promotions 
	FOR EACH ROW 
	begin
		if (select count(*) from employees where employee_id=new.employee_id ) = 0
		then
			signal sqlstate '45000'
			set message_text='erreur : cet employé n\'existe pas.';
		end if;
 	end;

insert into promotions (employee_id,old_job_title,new_job_title,old_salary,new_salary,promotion_date,reason,approved_by)
	values (210,'analyst','analyst senior',3000.00,	45000.00,'2025-02-26','promotion basé sur lancienté',114);

