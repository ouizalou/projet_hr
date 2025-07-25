use sample_rh;

-- TRIGGER : Vérifie que l'employé existe avant d'insérer une promotion
-- Objectif : Empêcher qu'on ajoute une promotion à un employé inexistant
DELIMITER $$

CREATE TRIGGER before_promotion_insert
BEFORE insert ON promotions 
	FOR EACH ROW 
	begin
		if (select count(*) from employes where id=new.employe_id ) = 0
		then
			signal sqlstate '45000'
			set message_text='erreur : cet employé n\'existe pas.';
		end if;
 	end;
DELIMITER $$

insert into promotions (employe_id,nouveau_poste_id,date_promotion,nouveau_salaire)
	values (124,3,'2025-02-26',45678);


-- TRIGGER : Empêche l'ajout d'une formation en doublon sur une même période
-- Objectif : éviter les chevauchements de formations similaires pour le même employé

DELIMITER $$

CREATE TRIGGER prevent_duplicate_formation
BEFORE INSERT ON formations
FOR EACH ROW
BEGIN
    DECLARE n INT;

    SELECT COUNT(*) INTO n FROM formations
    WHERE employe_id = NEW.employe_id
      AND titre = NEW.titre
      AND (
            NEW.date_debut BETWEEN date_debut AND date_fin
         OR NEW.date_fin BETWEEN date_debut AND date_fin
         OR date_debut BETWEEN NEW.date_debut AND NEW.date_fin
         OR date_fin BETWEEN NEW.date_debut AND NEW.date_fin
      );

    IF n > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : cet employé est déjà inscrit à cette formation sur la même période.';
    END IF;
END 
$$

DELIMITER ;

INSERT INTO formations (employe_id, titre, prestataire, date_debut, date_fin) VALUES (121, 'Innovate revolutionary functionalities', 'Test SARL', '2025-03-01', '2025-03-10');
