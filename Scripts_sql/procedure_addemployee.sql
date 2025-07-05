describe employees; 

use hr_sample;

-- DELIMITER //

-- procedure pour ajouter des employees 


create procedure addemployees(
	IN p_first_name varchar (20),
	IN p_last_name varchar (25),
	IN p_email varchar (100),
	IN p_phone_number varchar (20),
	IN p_hire_date DATE ,
	IN p_job_id int ,
	IN p_salary DECIMAL (8,2),
	IN p_manager_id int,
	IN p_department_id int
	)
begin
	insert into employees (first_name,last_name,email,phone_number,hire_date,job_id,salary,manager_id,department_id)
	values(p_first_name,p_last_name,p_email,p_phone_number,p_hire_date,p_job_id,p_salary,p_manager_id,p_department_id);
end ;
-- //
 
-- DELIMITER ;
 
# appel de la procedure addemployer pour ajouter des nouveaux employees
call addemployees(
	'axel', 'djebbarii', 'axel_djeb@gmail.com', '3356457823','2022-02-07', 9, 5000.00, 103 , 3
);
 call addemployees(
	'liza', 'lounas', 'liz_lou@gmail.com', '3369875467','2025-04-25', 9, 4500.00, 104 , 3
 );

call addemployees(
'tyty','lounas','tytylounas@yahoo.com','82167568790','2025-03-14',9,9800.00,105,3
);
select * from employees e where e.department_id =3 ;


