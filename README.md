# 👔 Base de Données RH

## 🧾 Description  
Cette base de données modélise de manière complète les processus liés aux Ressources Humaines. Elle permet de centraliser les données des employés, leur parcours professionnel, les services RH, ainsi que les indicateurs clés comme le turnover, la formation ou encore les absences. Elle est conçue pour répondre aux besoins stratégiques et opérationnels du service RH.

## 🗂️ Tables principales

| Table                   | Description                                                               |
|------------------------|---------------------------------------------------------------------------|
| `employes`             | Données personnelles et professionnelles des employés                     |
| `postes`               | Détails des postes, salaires min/max                                      |
| `departements`         | Répartition des employés par département                                  |
| `emplacements`         | Adresse, ville et code postal des départements                            |
| `regions`              | Regroupement géographique des emplacements                                |
| `pays`                 | Pays associés aux régions                                                 |
| `managers`             | Informations sur les responsables hiérarchiques                           |
| `salaries`             | Historique des salaires (net, brut, prime)                                |
| `absences`             | Historique des absences (type, dates, motif)                              |
| `promotions`           | Changements de poste et d’évolution salariale                             |
| `formations`           | Suivi des formations (titre, prestataire, durée)                          |
| `retraites`            | Données de retraite : date, âge, pension                                  |
| `rotation`             | Données de départs (date, raison, commentaire)                            |
| `dependants`           | Ayants droit (prénom, nom, lien, date naissance)                          |
| `reclamations_brutes`  | Réclamations RH soumises par les employés                                 |
| `clients`              | Clients de l’organisation (nom entreprise, contact, date de création)     |
| `services_rh`          | Prestations RH fournies aux clients                                       |


## 🎯 Besoins Métiers Couvert par la BDD RH

| Besoin RH                         | Objectif Métiers RH                                                     |
|---------------------------------- |-------------------------------------------------------------------------|
| 📊 Pilotage RH                   | Suivi des effectifs, âge moyen, ancienneté, pyramide des âges            |
| 📈 Analyse du Turnover           | Identifier les causes de départs, calcul du taux de rotation             |
| 💸 Suivi de la masse salariale   | Contrôle des coûts RH, prévisions budgétaires                            |
| 📚 Plan de formation             | Suivi des formations réalisées, conformité avec les obligations légales  |
| 🔁 Gestion de carrière           | Historique des promotions, accompagnement des évolutions internes        |
| 👪 Suivi  social                 | Suivi des ayants droit, conformité avec les obligations sociales         |
| 📍 Répartition géographique       | Localisation des effectifs, multi-sites, reporting local/national        |
| 🧾 Archivage et conformité       | Conformité RGPD, traçabilité RH                                          |
| 🧰 Prestations RH aux clients	   | Historique des services RH délivrés à chaque client                      |


## 🖼️ Schéma relationnel

diagramme/hr_sample_diagramme.png


## 📂 Arborescence du dépôt

```
hr_project/
│
├── script_python/           # Scripts Python pour l'analyse des données RH
├── diagramme/               # Schéma relationnel de la base de données
│   └── hr_sample_diagramme.png
├── README.md                # Présentation du projet RH
└── ...
```

## 📬 Contact

📧 ouizalou@gmail.com  
🐙 [GitHub - ouizalou](https://github.com/ouizalou)

---

🧠 *Projet pédagogique de modélisation RH — librement réutilisable pour des cas pratiques d’analyse ou d’audit RH.*
