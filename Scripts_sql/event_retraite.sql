use sample_rh;

alter table employes add column statut_retraite ENUM('actif', 'proche_retraite', 'retraité') DEFAULT 'actif';


-- activer le planificateur

SET GLOBAL event_scheduler = ON;

-- afficher le status scheduler

SHOW VARIABLES LIKE 'event_scheduler';


-- ✅ Création d’un événement planifié qui s’exécute toutes les minutes
-- Il met à jour le statut "proche_retraite" pour les employés ayant 58 à 59 ans et encore actifs

CREATE EVENT mark_proche_retraite
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
    UPDATE employes 
    SET statut_retraite = 'proche_retraite' 
    WHERE TIMESTAMPDIFF(YEAR, date_naissance, CURDATE()) >= 58
      AND TIMESTAMPDIFF(YEAR, date_naissance, CURDATE()) < 60
      AND statut_retraite = 'actif';
END;

-- ✅ Création d’un autre événement planifié
-- Il met à jour le statut "retraite" pour tous les employés ayant 60 ans ou plus
-- Peu importe s'ils sont encore "actif" ou déjà "proche_retraite"


CREATE EVENT mark_retraite
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
    UPDATE employes 
    SET statut_retraite = 'retraite' 
    WHERE TIMESTAMPDIFF(YEAR, date_naissance, CURDATE()) >= 60
      AND statut_retraite IN ('actif', 'proche_retraite');
END;

-- ✅ Requête pour afficher les employés ayant au moins 37 ans d'ancienneté
-- Permet par exemple de repérer ceux qui approchent de la retraite par ancienneté de service

select id, date_embauche, TIMESTAMPDIFF(YEAR, date_embauche, CURDATE()) as service_year 
from employes where TIMESTAMPDIFF(YEAR, date_embauche, CURDATE())>=37;
