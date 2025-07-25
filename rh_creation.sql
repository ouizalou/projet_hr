-- Création des tables RH avec clés primaires AUTO_INCREMENT
use sample_rh;
CREATE TABLE pays (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE regions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pays_id INT NOT NULL,
    nom VARCHAR(100) NOT NULL,
    FOREIGN KEY (pays_id) REFERENCES pays(id)
);

CREATE TABLE emplacements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    region_id INT NOT NULL,
    adresse VARCHAR(255) NOT NULL,
    code_postal VARCHAR(20),
    ville VARCHAR(100),
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

CREATE TABLE departements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    emplacement_id INT NOT NULL,
    nom VARCHAR(100) NOT NULL,
    FOREIGN KEY (emplacement_id) REFERENCES emplacements(id)
);

CREATE TABLE postes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    intitule VARCHAR(150) NOT NULL,
    salaire_min DECIMAL(10,2) NOT NULL,
    salaire_max DECIMAL(10,2) NOT NULL
);

CREATE TABLE employes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    departement_id INT NOT NULL,
    poste_id INT NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    telephone VARCHAR(50),
    date_embauche DATE,
    genre ENUM('Homme', 'Femme'),
    date_naissance DATE,
    FOREIGN KEY (departement_id) REFERENCES departements(id),
    FOREIGN KEY (poste_id) REFERENCES postes(id)
);

CREATE TABLE managers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    niveau ENUM('Senior', 'Middle', 'Junior'),
    date_promotion DATE,
    FOREIGN KEY (employe_id) REFERENCES employes(id)
);

CREATE TABLE salaires (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    salaire_brut DECIMAL(10,2),
    salaire_net DECIMAL(10,2),
    prime DECIMAL(10,2),
    date DATE,
    FOREIGN KEY (employe_id) REFERENCES employes(id)
);

CREATE TABLE absences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    type VARCHAR(50),
    date_debut DATE,
    duree_jours INT,
    motif VARCHAR(255),
    FOREIGN KEY (employe_id) REFERENCES employes(id)
);

CREATE TABLE promotions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    nouveau_poste_id INT NOT NULL,
    date_promotion DATE,
    nouveau_salaire DECIMAL(10,2),
    FOREIGN KEY (employe_id) REFERENCES employes(id),
    FOREIGN KEY (nouveau_poste_id) REFERENCES postes(id)
);

CREATE TABLE formations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    titre VARCHAR(255),
    prestataire VARCHAR(255),
    date_debut DATE,
    date_fin DATE,
    FOREIGN KEY (employe_id) REFERENCES employes(id)
);

CREATE TABLE retraites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    date_retraite DATE,
    age_retraite INT,
    montant_pension DECIMAL(10,2),
    FOREIGN KEY (employe_id) REFERENCES employes(id)
);

CREATE TABLE rotation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    date_depart DATE,
    raison VARCHAR(100),
    commentaire TEXT,
    FOREIGN KEY (employe_id) REFERENCES employes(id)
);

CREATE TABLE dependants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    prenom VARCHAR(100),
    nom VARCHAR(100),
    lien VARCHAR(50),
    date_naissance DATE,
    FOREIGN KEY (employe_id) REFERENCES employes(id)
);

CREATE TABLE clients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom_entreprise VARCHAR(255),
    contact VARCHAR(150),
    email VARCHAR(150),
    telephone VARCHAR(50),
    date_creation DATE
);

CREATE TABLE services_rh (
    id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT NOT NULL,
    type_service VARCHAR(100),
    date_prestation DATE,
    cout DECIMAL(10,2),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE reclamations_brutes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employe_id INT NOT NULL,
    sujet VARCHAR(100),
    date_reclamation DATE,
    description TEXT,
    FOREIGN KEY (employe_id) REFERENCES employes(id)
);
