
# =====================================================================================
# 📘 SCRIPT : Gestion des Formations des Employés
# 🗂️ Connexion à la base de données RH (MySQL)
# 🛠️ Utilisation de SQLAlchemy ORM pour la création et manipulation des données
# 👤 Auteur : [Votre nom]
# 📅 Date : [Date du jour]
# =====================================================================================

# ======================== des bibliothèques et des modules à importer ================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
# pour la connection a la base de donnees 
#  create_engine ==> crée la connexion
from sqlalchemy import create_engine,inspect, Column,Integer,String,Date,Enum,ForeignKey
# orm ==>manipuler les BDD avec des classes
# declarative_base ==> declarer des tables  pour créer des classes qui representent des tables de la base de données
# sessiomaker ==> créer es session pour intergir avec les BDD ( insertion , requete)  
from sqlalchemy.orm import declarative_base,sessionmaker
import pymysql

# ============================ informations de connexion a la base  Mysql ============================
host="localhost"
port="3306"
DB_name="hr_sample"
username="root"
password="root"

# ============================ creer une URL de connexion pour Mysql ===============================

try:
    engine=create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{DB_name}')
    connection=engine.connect()
    print("\n ✅  la connexion est bien réussie a la base de données ")

# ======================== connexion a la base de données RH ====================================
    # lister les tables de la base de données avec inspect
    # la methode inspect permet de d'inspecter la structure de la abase de données (tables, colonnes , types , clés primaires)
    inspector=inspect(engine)
    # listes des tables existantes 
    tables=inspector.get_table_names()
    print("\n 📋 Tables disponibles :")
    for table in tables:
        print(f" -{table}")

    # afficher les 5 premiers lignes de chaque table
    for table in tables:
        print(f"\n 🔍 Aperçu des 5 premiers lignes de la table : {table}")
        DF=pd.read_sql(f"select * from {table} limit 5",engine)
        print(DF)
    # afficher les colonnes des  tables 
    columns=inspector.get_columns('employees')
    print("\n 🧱 les colonnes de la table employees :")
    for column in columns:
        print(f"- {column['name']}({column['type']})")
except Exception as e:
    print("\n❌ error lors de la connexion a la base de données ")
    print (e)
    # lecture d'une table de la base de données
print("\n le contenu de la tabe employees :\n")
DF_employee=pd.read_sql('select * from employees', engine)
print(DF_employee.head())

print("\n le contenu de la tabe regions :\n")
DF_regions=pd.read_sql('select * from regions',engine)
print(DF_regions.head())

try:
    # definir  la table formation avec ORM
    # declaration de la base ORM
    Base=declarative_base()
    # declaration de la class employee
    # Classe de liaison minimale pour définir la table employees (juste pour permettre la clé étrangère).
    class employees(Base):
        __tablename__='employees'
        employee_id=Column(Integer,primary_key=True)
    # declaration de la classe Formation 
    class formations(Base):
        __tablename__='formations'
        formation_id=Column(Integer,primary_key=True,autoincrement=True)
        employee_id =Column(Integer,ForeignKey('employees.employee_id'))
        titre=Column(String(100))
        organisme=Column(String(250))
        date_begin=Column(Date)
        date_end=Column(Date)
        statut=Column(Enum('en cours','terminé','abondonnée',name='formation_statut'))
   
    # Crée physiquement la table formations dans la base de données.
    Base.metadata.create_all(engine)
    print("\n la table formations a bien été créer ")
    # Crée une session pour interagir avec la base de données.
    Session = sessionmaker(bind=engine)
    session = Session()

    """ new_formation=formations(
        employee_id=114,
        titre="Analyse de données en python",
        organisme="openclassrooms",
        date_begin="2024-01-01",
        date_end="2024-05-31",
        statut="terminé"
    )
    session.add(new_formation)
    session.commit()"""
    #  fonction d'insertion de données dans la table formation 
    def ajouter_formation(session,liste_formations):
        try:
            objets_fotmations=[
                formations(
                    employee_id=donnee['employee_id'],
                    titre =donnee['titre'],
                    organisme=donnee['organisme'],
                    date_begin=donnee['date_begin'],
                    date_end=donnee['date_end'],
                    statut=donnee['statut']
                )
                for donnee in liste_formations
            ]
            session.add_all(objets_fotmations)
            session.commit()
            print("\✅ formation ajoutées avec succès")
        except Exception as e:
            session.rollback()
            print("❌ erreur lors d'insertion ",e)
    def lire_formations(session):
        try:
            # requete pour lire toutes les lignes de la table formations
            resultats=session.query(formations).all()
            print("\n 📄 Liste des formations enregistrées :\n")
            for formation in resultats:
                print(f"ID:{formation.formation_id},Employé:{formation.employee_id},"
                      f"Titre:{formation.titre},Organisme:{formation.organisme}",
                      f"statut:{formation.statut}")
        except Exception as e:
            print("❌ Erreur lors de la lecture des données :", e)

# ============================================ filtrer les données ========================================

    def filtrer_formations(session,statut=None):
        try:
            requete=session.query(formations)
            if statut:
                requete=requete.filter(formations.statut==statut)
            resultats=requete.all()
            print("\n🔍 Résultats du filtre :\n")
            if not resultats:
                print("Aucune formation trouvée avec les critères donnés.")
            else:
                for formation in resultats:
                    print(f"- ID: {formation.formation_id},"
                        f"Employé: {formation.employee_id},"
                        f" Titre: {formation.titre}, "
                        f"Organisme: {formation.organisme},"
                        f"Début: {formation.date_begin},"
                        f"Fin: {formation.date_end},"
                        f"Statut: {formation.statut}")
        except Exception as e:
            print("❌ Erreur lors du filtrage :", e)

except Exception as e:
    print("\n erreur d'insertion de données ")

# =================================== exmple d'insertion dans la table formation =================================

# liste_formations == > une liste de dictionnaires // chaque dictionnaire est une formation
liste_formations=[
    {
        'employee_id':114,
        'titre':'Analyse de données en python',
        'organisme':'openclassrooms',
        'date_begin':'2024-01-01',
        'date_end':'2024-05-31',
        'statut':'terminé'
    },
    { 
        'employee_id':102,
        'titre':'management',
        'organisme':'classrooms',
        'date_begin':'2024-08-14',
        'date_end':'2024-10-30',
        'statut':'terminé'
    },
    {
        'employee_id':101,
        'titre':'marketing',
        'organisme':'learning linkedin',
        'date_begin':'2025-03-03',
        'date_end':'2025-05-30',
        'statut':'en cours'
    },
    {
        'employee_id':104,
        'titre':'communication interpersonnelle',
        'organisme':'learning linkedin',
        'date_begin':'2025-03-03',
        'date_end':'2025-04-30',
        'statut':'abondonnée'
    }

]
# ajout des formation 
ajouter_formation(session,liste_formations)

# lecture des formations
lire_formations(session)

# Filtrer les formations "terminé" 
filtrer_formations(session,statut="terminé")
