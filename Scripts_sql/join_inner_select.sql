  use HR_SAMPLE;
  
  -- les jointeurs permettent dassocier plusieurs tables dans une meme requete

    select * from departments inner join employees on departments.department_id = employees.department_id;
    
    -- afficher  les departement qui ont la au moins une location
    
    select locations.location_id,department_id, department_name, street_address,city, state_province from locations 
    inner join departments on locations.location_id = departments.location_id;
    
    -- afficher les  departement de seattle
    
    select l.location_id, d.department_id, d.department_name,l.street_address,l.state_province,l.city 
    from locations l inner join departments d on l.location_id = d.location_id where l.city= 'seattle';
      
      -- afficher les employees de chaque departement et son job
    
    select d.department_id, d.department_name, e.employee_id ,e.first_name,e.last_name,e.salary,e.hire_date, 
    j.job_title from employees e inner join departments d on e.department_id = d.department_id
    inner join jobs j on e.job_id = j.job_id ;
    
    -- afficher les employees qui travaillent dans le department purchasing et leurs job title
    
       select d.department_id, d.department_name, e.employee_id ,e.first_name,e.last_name,e.salary,e.hire_date, 
    j.job_title from employees e inner join departments d on e.department_id = d.department_id
    inner join jobs j on e.job_id = j.job_id  where d.department_name = 'purchasing';
    
    -- afficher toutes le ligne de la table parent a gauche (managers)
    
    select d.department_id, d.department_name, m.manager_id , m.first_name,m.last_name, m.hire_date,m.salary 
     from managers m left join departments d on m.department_id = d.department_id ;
    
    
	select e.employee_id ,e.first_name,e.last_name,e.salary,e.hire_date, d.department_id, d.department_name, 
    m.first_name,m.hire_date ,m.manager_id from employees e left join departments d on e.department_id = d.department_id
    left join managers m on e.manager_id = m.manager_id;
    
    -- afficher toute les donnees de la table a droite(departement)
    
	 select d.department_id, d.department_name, m.manager_id , m.first_name,m.last_name, m.hire_date,m.salary 
     from managers m right join departments d on m.department_id = d.department_id  ;
    
    select e.employee_id ,e.first_name,e.last_name,e.salary,e.hire_date, d.department_id, d.department_name, 
    m.first_name,m.hire_date ,m.manager_id from employees e left join departments d on e.department_id = d.department_id
    left join managers m on e.manager_id = m.manager_id where e.manager_id is null;
    
    
    select country_name, city,region_name from locations l right join countries c on c.country_id=l.country_id 
    right join regions r on c.region_id= r.region_id order by city, country_name;
    
   -- relier une table pour afficher les supervisor des mangers qui sont eux memes des manages (auto jointure-self join)

    
   select t1.first_name as manager_name,t1.manager_id as manager_id,t2.first_name as supervisor_name,t2.manager_id 
   as supervisor_id from managers  as t1 left join managers as t2
   on t1.supervisor_id=t2.manager_id;
   
   -- affichers toutes les lignes des deux tables concernees ,quil avait de correspondance ou pas
    -- full outer join (union left et right join )
   
   select e.employee_id,e.first_name, m.manager_id, m.salary  from employees e
   left  join managers m on e.manager_id= m.manager_id
   union
       select e.employee_id,e.first_name, m.manager_id, m.salary  from employees e
   right  join managers m on e.manager_id= m.manager_id;
   
   --  renvoie toute les combinaison possible entre les lignes des deux table 
   select e.employee_id, e.first_name, d.department_id, d.department_name from employees e cross join departments d;
   

