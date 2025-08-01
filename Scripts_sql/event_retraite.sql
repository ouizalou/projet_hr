use sample_rh;

alter table employes add column statut_retraite ENUM('actif', 'proche_retraite', 'retraité') DEFAULT 'actif';


-- activer le planificateur

SET GLOBAL event_scheduler = ON;

-- afficher le status scheduler

SHOW VARIABLES LIKE 'event_scheduler';


-- ⏳ ÉVÉNEMENT : mise à jour du statut "proche_retraite"
-- ▶️ Objectif : tous les employés ayant entre 58 et 59 ans, encore actifs, passent à "proche_retraite"

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

-- 🎯 ÉVÉNEMENT : mise à jour du statut "retraite"
-- ▶️ Objectif : tous les employés de 60 ans ou plus deviennent "retraité"

CREATE EVENT mark_retraite
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
    UPDATE employes 
    SET statut_retraite = 'retraite' 
    WHERE TIMESTAMPDIFF(YEAR, date_naissance, CURDATE()) >= 60
      AND statut_retraite IN ('actif', 'proche_retraite');
END;

-- 🧓 Requête : employés avec 37 ans d’ancienneté ou plus
-- ▶️ Objectif : repérer les employés proches de la retraite par ancienneté

select id, date_embauche, TIMESTAMPDIFF(YEAR, date_embauche, CURDATE()) as service_year 
from employes where TIMESTAMPDIFF(YEAR, date_embauche, CURDATE())>=37;

-- ⚠️ ÉVÉNEMENT NON VALIDE : sélection directe non autorisée dans un événement
-- ▶️ Cette requête doit être insérée dans une table temporaire ou appel à une procédure stockée
-- ❌ Ce bloc ne fonctionnera pas tel quel

CREATE EVENT event_reclamation_alert
ON SCHEDULE EVERY 1 DAY
DO
BEGIN
    SELECT employe_id, COUNT(*) AS nb_reclamations
    FROM reclamations_brutes
    WHERE date_reclamation >= CURDATE() - INTERVAL 30 DAY
    GROUP BY employe_id
    HAVING nb_reclamations >= 3;
END;

-- 📝 ÉVÉNEMENT : ajout automatique des retraités dans la table retraites
-- ▶️ Objectif : inscrire dans la table retraites tout employé nouvellement retraité (60 ans+)

CREATE EVENT insert_retraites_auto
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
    INSERT INTO retraites (employe_id, date_retraite, age_retraite, montant_pension)
    SELECT 
        id, CURDATE(), TIMESTAMPDIFF(YEAR, date_naissance, CURDATE()), salaire_net * 0.75
    FROM employes e
    JOIN salaires s ON s.employe_id = e.id
    WHERE TIMESTAMPDIFF(YEAR, date_naissance, CURDATE()) >= 60
      AND NOT EXISTS (
        SELECT 1 FROM retraites r WHERE r.employe_id = e.id
      );
END;

-- 📊 ÉVÉNEMENT : calcul annuel du turnover
-- ▶️ Objectif : insérer chaque année le nombre de départs de l'année précédente dans une table dédiée

CREATE EVENT update_annual_turnover
ON SCHEDULE EVERY 1 YEAR
STARTS '2025-07-25 14:00:00'
DO
BEGIN
    INSERT INTO annual_turnover (year, total_exits)
    SELECT 
        YEAR(CURDATE()) - 1,
        COUNT(*)
    FROM rotation
    WHERE YEAR(date_depart) = YEAR(CURDATE()) - 1;
END;

