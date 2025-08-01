  use sample_rh;
  
  -- les jointeurs permettent dassocier plusieurs tables dans une meme requete

    select * from departements inner join employes on departements.id = employes.departement_id;
    
    -- afficher  les departement qui ont la au moins une location
    
    select em.id, nom, adresse,code_postal, ville 
    from emplacements em
    inner join departements d on em.id = d.emplacement_id;
    
    -- afficher les  departement de seattle
    
    select em.id, d.id as departement_id, d.nom,em.adresse,em.code_postal,em.ville 
    from emplacements em
    inner join departements d on em.id = d.emplacement_id where em.ville= 'Lake Oliviatown';
      
      -- afficher les employees de chaque departement et son job
    
    select d.id as departement_id, e.id as employe_id ,e.nom,e.prenom,e.telephone,e.date_embauche,  d.nom,
    p.intitule
    from employes e 
    inner join departements d on e.departement_id = d.id
    inner join postes p on e.poste_id = p.id ;
    
    -- afficher les employees qui travaillent dans le department purchasing et leurs job title
    
       select d.id, d.nom, e.id ,e.nom,e.prenom,e.telephone,e.date_embauche, 
    p.intitule from employes e 
    inner join departements d on e.departement_id = d.id
    inner join postes p on e.poste_id = p.id  where d.nom = 'Productize vertical mindshare';
    
    -- afficher toutes le ligne de la table parent a gauche (managers)
    
    select e.id as employe_id, e.nom,e.prenom, m.id as manager_id , m.niveau, m.date_promotion
     from managers m left join employes e on m.employe_id = e.id ;
    
    
	select e.id as employe_id ,e.nom,e.prenom,e.telephone,e.date_embauche, d.id as departement_id, d.nom as nom_daratement, 
    m.niveau,m.date_promotion ,m.id as manager_id 
    from employes e
    left join departements d on e.departement_id = d.id
    left join managers m on m.employe_id = e.id;
    
    -- afficher toute les donnees de la table a droite(departement)
    
	 select d.id as departement_id, d.nom as nom_departement, em.adresse, em.ville, r.nom as nom_region
     from emplacements em 
	 right join departements d on d.emplacement_id = em.id
	 right join regions r on em.region_id=r.id;
	
    
    select e.id as employe_id ,e.nom,e.prenom,e.statut_retraite,e.date_embauche, d.id as departement_id, d.nom as nom_departement, 
    m.niveau,m.date_promotion ,m.id as manager_id 
    from employes e
    left join departements d on e.departement_id = d.id
    left join managers m on m.employe_id=e.id;    
    
    select r.id as region_id,r.nom as region_name , p.nom as pays
    from pays p 
    right join regions r on p.id=r.pays_id;
  
   
   -- affichers toutes les lignes des deux tables concernees ,quil avait de correspondance ou pas
    -- full outer join (union left et right join )
   
   select e.id as employe_id,e.nom, m.id as manager_id, m.niveau  
   from employes e
   left  join managers m on m.employe_id= e.id
   union
       select e.id as employe_id,e.nom, m.id as manager_id, m.niveau  
       from employes e
   right  join managers m on m.employe_id= e.id;
   
   --  renvoie toute les combinaison possible entre les lignes des deux table 
   select e.id as employee_id, e.nom, e.prenom ,d.id as departement_id, d.nom as nom_departement 
   from employes e cross join departements d;
   

