# data_analyst
data-analyst-work
# Base de données Base de Données RH

## Description
Cette base de données modélise de manière complète les processus liés aux Ressources Humaines. Elle permet de centraliser les données des employés, leur parcours professionnel, les services RH,
ainsi que les indicateurs clés comme le turnover, la formation ou encore les absences. Elle est conçue pour répondre aux besoins stratégiques et opérationnels du service RH.

## 🗂️ Tables principales

| Table                   | Description                                               |
|-------------------------|-----------------------------------------------------------|
| `employees`             | Données personnelles et professionnelles des employés    |
| `jobs`                  | Détails des postes, salaires minimum et maximum           |
| `departments`           | Structure organisationnelle interne                        |
| `locations`             | Localisation des départements                              |
| `managers`              | Informations sur les superviseurs                          |
| `salaries`              | Historique des paies : brut, net, taxes                   |
| `absences`              | Historique des absences (type, durée, motif)              |
| `promotions`            | Changements de poste et évolutions salariales             |
| `formations`            | Suivi des formations, dates et organismes                  |
| `retirements`           | Départs à la retraite, âge, pension                        |
| `turnover`              | Départs d’employés, feedback, raisons                      |
| `dependents`            | Ayants droit liés à un employé                             |
| `clients`               | Entreprises clientes dans un contexte de prestations RH   |
| `hr_services`           | Services RH délivrés aux clients                           |
| `claims_raw`            | Réclamations ou incidents RH signalés                      |
| `regions`, `countries`  | Hiérarchie géographique                                    |

# 🖼️ Schéma relationnel (Mermaid) 
![diagram _ RH](https://github.com/user-attachments/assets/3d696628-31b3-4bd9-9b2b-57b2297c0f33)



