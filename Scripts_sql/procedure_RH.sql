use sample_rh;

/*
 * Procédure : addemployees
 * Objectif : Ajouter un employé avec ses informations de base
 * Utilité : Permet de créer un dossier RH dès le recrutement
 */

DELIMITER //

create procedure addemployees(
	IN p_poste_id int,
	IN p_departement_id int,
	IN p_prenom varchar (100),
	IN p_nom varchar (100),
	IN p_email varchar (150),
	IN p_telephone varchar (50),
	IN p_date_embauche DATE ,
	IN p_genre enum('Homme','Femme') ,
	IN p_date_naissance DATE
	)
begin
	insert into employes (poste_id,departement_id,prenom,nom,email,telephone,date_embauche,genre,date_naissance)
	values (p_poste_id,p_departement_id,p_prenom,p_nom,p_email,p_telephone,p_date_embauche,p_genre,p_date_naissance);
end ;
//
DELIMITER ;
 
call addemployees(
87,12,'Arezeki','lounas','arezekilolounas@yahoo.com','8219478391','2021-08-30','Homme', '1992-01-07'
); 



/*
 * Procédure : record_absence
 * Objectif : Ajouter une absence pour un employé
 * Utilité : Suivi des congés, maladies, absences injustifiées...
 */

DELIMITER //
CREATE PROCEDURE record_absence(
	IN p_employe_id INT,
	IN p_type VARCHAR(50),
	IN p_date_debut DATE,
	IN p_duree_jours INT,
	IN p_motif TEXT
)
BEGIN
	IF EXISTS (SELECT 1 FROM employes WHERE id = p_employe_id) THEN
		INSERT INTO absences(employe_id, type, date_debut, duree_jours, motif)
		VALUES (p_employe_id, p_type, p_date_debut, p_duree_jours, p_motif);
	ELSE
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Employé introuvable.';
	END IF;
END;
//
DELIMITER ;

call record_absence(109,'Maladie','2024-09-12',10,'hospitalise');



/*
 * Procédure : get_total_absence_by_employee
 * Objectif : Obtenir le total des jours d'absence pour un employé donné
 * Utilité : Contrôle des absences, gestion du présentéisme
 */

DELIMITER //
CREATE PROCEDURE get_total_absence_by_employee(IN p_employe_id INT)
BEGIN
	SELECT 
		e.id AS employe_id,
		e.nom,
		e.prenom,
		IFNULL(SUM(a.duree_jours), 0) AS total_absences
	FROM employes e
	LEFT JOIN absences a ON e.id = a.employe_id
	WHERE e.id = p_employe_id
	GROUP BY e.id;
END;
//
DELIMITER ;

call get_total_absence_by_employee(109);

/*
 * Procédure : add_formation
 * Objectif : Ajouter une formation suivie par un employé
 * Utilité : Gestion de la montée en compétence et du plan de formation
 */

DELIMITER //
CREATE PROCEDURE add_formation(
	IN p_employe_id INT,
	IN p_titre VARCHAR(150),
	IN p_prestataire VARCHAR(150),
	IN p_date_debut DATE,
	IN p_date_fin DATE
)
BEGIN
	IF EXISTS (SELECT 1 FROM employes WHERE id = p_employe_id) THEN
		INSERT INTO formations(employe_id, titre, prestataire, date_debut, date_fin)
		VALUES (p_employe_id, p_titre, p_prestataire, p_date_debut, p_date_fin);
	ELSE
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Employé introuvable.';
	END IF;
END;
//
DELIMITER ;

call add_formation(171,'Scale visionary synergies','Hamon Laporte SARL','2023-11-03','2024-08-10');

/*
 * Procédure : add_dependant
 * Objectif : Ajouter une personne à charge (enfant, conjoint...)
 * Utilité : Avantages sociaux, couverture mutuelle, gestion famille
 */

DELIMITER //
CREATE PROCEDURE add_dependant(
	IN p_employe_id INT,
	IN p_prenom VARCHAR(100),
	IN p_nom VARCHAR(100),
	IN p_lien VARCHAR(50),
	IN p_date_naissance DATE
)
BEGIN
	IF EXISTS (SELECT 1 FROM employes WHERE id = p_employe_id) THEN
		INSERT INTO dependants(employe_id, prenom, nom, lien, date_naissance)
		VALUES (p_employe_id, p_prenom, p_nom, p_lien, p_date_naissance);
	ELSE
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Employé introuvable.';
	END IF;
END;
//
DELIMITER ;
call add_dependant(192,'gaya','djebar','fils','2025-01-15');


/*
 * Procédure : generate_annual_rh_report
 * Objectif : Générer un rapport RH pour une année donnée
 * Utilité : Suivi annuel des effectifs, absences, promotions, départs
 */

DELIMITER //

CREATE PROCEDURE generate_annual_rh_report(IN p_year INT)
BEGIN

	-- 1. Nombre d’employés actifs au 1er janvier et au 31 décembre
	SELECT 
		(SELECT COUNT(*) 
		 FROM employes e 
		 WHERE e.date_embauche <= STR_TO_DATE(CONCAT(p_year, '-01-01'), '%Y-%m-%d')
		   AND (e.statut_retraite IS NULL OR e.statut_retraite = 'Non')) AS total_debut_annee,

		(SELECT COUNT(*) 
		 FROM employes e 
		 WHERE e.date_embauche <= STR_TO_DATE(CONCAT(p_year, '-12-31'), '%Y-%m-%d')
		   AND (e.statut_retraite IS NULL OR e.statut_retraite = 'Non')) AS total_fin_annee;

	-- 2. Total des absences par employé sur l’année
	SELECT 
		e.id AS employe_id,
		e.nom,
		e.prenom,
		IFNULL(SUM(a.duree_jours), 0) AS total_absences
	FROM employes e
	LEFT JOIN absences a 
		ON e.id = a.employe_id 
		AND YEAR(a.date_debut) = p_year
	GROUP BY e.id;

	-- 3. Promotions dans l’année
	SELECT 
		p.employe_id,
		e.nom,
		e.prenom,
		COUNT(*) AS nb_promotions
	FROM promotions p
	JOIN employes e ON p.employe_id = e.id
	WHERE YEAR(p.date_promotion) = p_year
	GROUP BY p.employe_id;

	-- 4. Départs (rotation) dans l’année
	SELECT 
		YEAR(r.date_depart) AS annee,
		COUNT(*) AS total_departures
	FROM rotation r
	WHERE YEAR(r.date_depart) = p_year
	GROUP BY annee;

END;
//

DELIMITER ;
call generate_annual_rh_report(2020);
