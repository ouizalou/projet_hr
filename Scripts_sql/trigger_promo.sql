

-- 🔄 Sélection de la base de données

USE hr_sample;

-- ⚠️ Déclencheur (trigger) pour bloquer les insertions invalides dans la table "promotions"
-- Objectif : empêcher d'ajouter une promotion si l'employé (employee_id) n'existe pas
-- dans la table "employees"

CREATE TRIGGER before_promotion_insert
BEFORE INSERT ON promotions   -- Avant chaque insertion dans "promotions"
FOR EACH ROW                  -- Pour chaque ligne insérée
BEGIN
    -- Vérifie si l'employee_id fourni existe bien dans la table "employees"
    IF (
        SELECT COUNT(*) 
        FROM employees 
        WHERE employee_id = NEW.employee_id
    ) = 0
    THEN
        -- Si l'employee_id n'existe pas, on déclenche une erreur personnalisée
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : cet employé n\'existe pas.';
    END IF;
END;


INSERT INTO promotions (
    employee_id,
    old_job_title,
    new_job_title,
    old_salary,
    new_salary,
    promotion_date,
    reason,
    approved_by
)
VALUES (
    210,
    'analyst',
    'analyst senior',
    3000.00,
    45000.00,
    '2025-02-26',
    'promotion basée sur l\'ancienneté',
    114
);
