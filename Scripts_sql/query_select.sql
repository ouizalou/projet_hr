
 use HR_SAMPLE;
 -- condition where and or 
select first_name ,last_name ,salary from employees where salary >5000;
select first_name ,last_name ,salary from employees where salary >5000 and department_id= 9;
select first_name ,last_name ,salary from employees where salary >5000 or department_id <5;

  -- between pour filtrer des resultats dans  une plage de valeur
select * from jobs where max_salary between 9000.00 and 10000.00;

-- rechercher des modeles dans une chaine de caractere avec where et like 

select * from jobs where job_title like 'Ac%';
select * from employees where first_name like '_a%';
select * from departments where department_name like 'IT';
select * from locations where state_province like '%ia';

-- where and is 

select * from employees where phone_number is null;

select * from employees where phone_number is not null;


 -- rennomer une colonne ou une table tomporairement
 
select first_name as ' nom' from employees ; 

 -- la table employees est renommee tomporairement en e- * utilisation dun alias
 
 select e.email from employees as e;
 
 -- afficher nombre de ligne avec la fonction count sous le nom nombre total tomporairement

select count(*)  as 'employees_number' from employees;

 -- trier les resultats dune requette en foction de colonne ou plusieurs
select hire_date , salary from employees  order by salary asc; -- croissant
select hire_date , salary from employees  order by hire_date desc;-- decroissant

 -- trier en utilisant une foction et colonne tomporaire avec as
 
select max_salary, max_salary*2 as 'depense' from jobs order by depense asc;

-- retourner nombre total d'investissement
 
 select count(*) from departments;
 
  -- rechercher une valeur dans une liste  
select * from employees where department_id in(3, 6,10);
select * from employees where job_id in(2, 6,10, 14);
select * from HR_SAMPLE.countries where region_id in(2, 1,4) order by region_id asc;

 -- extraire une partie dune date annee ou jour ou mois 
 
select first_name,last_name, hire_date, extract(month from hire_date) as mois 
  from HR_SAMPLE.employees where extract(month from hire_date) IN (1, 2, 3) order by mois;
  
select first_name ,hire_date , extract(day from hire_date) as jour from HR_SAMPLE.employees
  where extract(day from hire_date) in (4,5,15) order by jour asc;
  -- not in
select first_name ,hire_date , extract(year from hire_date) as annee from HR_SAMPLE.employees
  where extract(year from hire_date)  not in (1994,2001,1999,1987) order by annee asc;
  
  -- afficher des valeurs unique avec distinct
  
   select distinct relationship from HR_SAMPLE.dependents ;
   
	select distinct salary, job_id from HR_SAMPLE.employees order by  job_id, salary desc ;

   
-- afficher un certain nombre de ligne --limit-- a partir dune position specifique --offset--
   
   select * from employees limit 5;  -- afficher 05 premier ligne 
   
   select * from employees limit 5 offset 4; -- afficher 05 ligne a partir position 4
   
   select  employee_id, first_name, last_name, salary from employees 
   order by salary desc limit 10 offset 20;
   
     select distinct e.employee_id, e.first_name, last_name, salary from employees e 
    order by salary limit 1 offset 1;
    
   
        -- function max , min 
 select max(salary) from employees;
 select min(salary) from employees;
 select max(salary) as salaire_max from employees ;
 select min(salary) as salaire_minimum from employees;
 select min(hire_date) from employees;

  -- retourner nombre de ligne count
  
  select count(*) as jobs_number from jobs ;
  select count(country_id) as number_contries from countries;
  
  -- retourner la somme des valeurs dune colonne 
  
   select sum(salary) as depense from employees;
   select sum(salary) +1500 as depense from employees where hire_date 
   between '1987-01-01' and '1990-01-01' ;
   
   -- calculer la moyenne dune colonne numerique
   
   select avg(max_salary) as moyenne from jobs;
   select avg(salary) as moyenne from employees where salary >15000.00 and department_id =9;
   
   -- utiliser case clause 
   
   select distinct job_title, 
     case 
      when max_salary = 30000.00 then 'senior'
      when max_salary <= 6000.00 then 'stage job'
      when max_salary between 7000.00 and 12000.00 then 'junior'
      when max_salary between 13000.00 and 29000.00 then 'expert'
      else 'president'
      end as status_job
	 from jobs;
      
      
      SELECT country_name, 
       CASE Country_name
         WHEN 'Australia' THEN 'English'
         WHEN 'Brazil' THEN 'Portuguese'
         WHEN 'Canada' THEN 'English'
         WHEN 'Denmark' THEN 'Danish'
         WHEN 'Finland' THEN 'Finnish'
         WHEN 'France' THEN 'French'
         WHEN 'Germany' THEN 'German'
         WHEN 'Italy' THEN 'Italian'
         WHEN 'Japan' THEN 'Japanese'
         WHEN 'Netherlands' THEN 'Dutch'
         WHEN 'Norway' THEN 'Norwegian'
         WHEN 'Singapore' THEN 'English'
         WHEN 'Spain' THEN 'Spanish'
         WHEN 'Sweden' THEN 'Swedish'
         WHEN 'UK' THEN 'English'
         WHEN 'USA' THEN 'English'
         else 'english '
       END AS Language 
  FROM countries;
   
   
   -- in avec sous requete -- afficher les employees travaillant dns les departemts a lacation 1400

   select * from employees where department_id in
   (select department_id from departments where location_id =1400);
    
    -- regrouper des lignes ayant des valeurs similaires selon une fonctio
      
       -- salaire moyenne des salaire par departemet
      
    select department_id, avg(salary) as salaire_moyenne from employees 
    group by department_id;
     
      -- nombre demployee par departement(regroupee par departement)
      
	select department_id, count(*) as number_employee from employees 
    group by department_id; 
    
      -- le salaire le plus bas et le salaire le plus haut par department
      
      select department_id , max(salary)as salaire_plus_haut, min(salary) as salire_plus_bas
      from employees group by department_id;
    
      -- salaire total par department
      
      select  department_id, sum(salary) as salaire_total
      from employees group by department_id;
      
      -- permet dutiliser plusieurs regroupement different (grouping set) sur mysql union all
      
      select d.department_name ,j.job_title, sum(e.salary) as tatal_salary from employees e join departments d
      on e.department_id=d.department_id join jobs j on e.job_id=j.job_id
      group by d.department_name,j.job_title
      union all
      select d.department_name, null as job_title, sum(e.salary) as total_salary from employees e 
      join departments d on e.department_id=d.department_id
      group by d.department_name;
        
        -- obtinir des sous-totaux et un total general ou les colonnes regroupent devient null pour indique agregation
        -- intermidire (sous-totaux et le total general
        
      select d.department_name ,j.job_title, sum(e.salary) as tatal_salary from employees e join departments d
      on e.department_id=d.department_id join jobs j on e.job_id=j.job_id
      group by d.department_name,j.job_title with rollup;
      
	  select d.department_name ,j.job_title, max(e.salary) as tatal_salary from employees e join departments d
      on e.department_id=d.department_id join jobs j on e.job_id=j.job_id
      group by d.department_name,j.job_title with rollup;
      
	
      -- nombre demployee pour chaque job
            
      
     select job_id , count(*) as _nombre_employe from employees
     group by job_id;
     
     -- le salaire moyenne par encienneté
     select  
        case 
        when hire_date between '1987-01-01' and '1995-01-01' then 'senior'
        when hire_date between '1996-01-01' and '2000-01-01' then 'junior' 
        else 'apprent'
         end as enciennete,
         avg(salary) as salire_moyenne
         from employees group by enciennete;
    
    -- filtrer nombre de pays par region ou nombre de payees >5
   
     select region_id, count(country_name) as numbre_pays from countries 
     group by region_id
     having count(country_id)> 2;
     
     -- salaire moyenne des salaire par departemet ou le salire moyenne > 9000.00
      
    select department_id, avg(salary) as salaire_moyenne from employees 
    group by department_id
    having avg(salary)> 9000.00
    order by department_id;
    
     -- combiner les resultats de plusieurs requetes (le meme nombre de colone et le meme type dans les requetes
     
     select country_name, region_id from countries where region_id =4 
     union
     select first_name, job_id from employees where hire_date between '1985-01-01' and '2000-01-01'
     order by country_name asc;
     
     -- retourner les employees ayant un salaire superieurs aux salaire de departement(reseltat de sous requete)
     
	select first_name, last_name,salary from employees where salary > 
    any(select salary from employees where department_id=10);
    
    -- retourner les employees dont le salaire est superier au salaire retournees par la sous requete
	select first_name, last_name,salary from employees where salary > 
    all (select salary from employees where department_id=8);
     
         select salary from employees where department_id=8;

     



