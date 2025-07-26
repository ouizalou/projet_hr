# =====================================================================================
# 📘 SCRIPT : Gestion des congés des Employés
# 🗂️ Connexion à la base de données RH (MySQL)
# 🛠️ Utilisation de SQLAlchemy ORM pour la création et manipulation des données
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
DB_name="sample_rh"
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
    columns=inspector.get_columns('employes')
    print("\n 🧱 les colonnes de la table employes :")
    for column in columns:
        print(f"- {column['name']}({column['type']})")
except Exception as e:
    print("\n❌ error lors de la connexion a la base de données ")
    print (e)
    # lecture d'une table de la base de données
print("\n le contenu de la tabe employees :\n")
DF_employee=pd.read_sql('select * from employes', engine)
print(DF_employee.head())

print("\n le contenu de la tabe regions :\n")
DF_regions=pd.read_sql('select * from regions',engine)
print(DF_regions.head())

try:
    # definir  la table congés avec ORM
    # declaration de la base ORM
    Base=declarative_base()
    # declaration de la class employee
    # Classe de liaison minimale pour définir la table employees (juste pour permettre la clé étrangère).
    class employes(Base):
        __tablename__='employes'
        id=Column(Integer,primary_key=True)
    # declaration de la classe congés 
    class conges(Base):
        __tablename__='conges'
        id=Column(Integer,primary_key=True,autoincrement=True)
        employe_id =Column(Integer,ForeignKey('employes.id'))
        type_conge=Column(String(20))
        date_debut=Column(Date)
        date_fin=Column(Date)
        statut=Column(Enum('en cours','validé','refusé','en attente','terminé',name='conge_statut'))

   
    # Crée physiquement la table congés dans la base de données.
    Base.metadata.create_all(engine)
    print("\n la table conges a bien été créer ")
    # Crée une session pour interagir avec la base de données.
    Session = sessionmaker(bind=engine)
    session = Session()

    """ new_conge=conges(
        employe_id=14,
        type_conge="Congé maternité",
        date_debut="2024-01-01",
        date_fin="2024-04-29",
        statut="terminé"
    )
    session.add(new_conge)
    session.commit()"""
    #  fonction d'insertion de données dans la table congés 
    def ajouter_conge(session,liste_conges):
        try:
            objets_conges=[
                conges(
                    employe_id=donnee['employe_id'],
                    type_conge =donnee['type_conge'],
                    date_debut=donnee['date_debut'],
                    date_fin=donnee['date_fin'],
                    statut=donnee['statut']
                )
                for donnee in liste_conges
            ]
            session.add_all(objets_conges)
            session.commit()
            print("\✅ conge ajoutées avec succès")
        except Exception as e:
            session.rollback()
            print("❌ erreur lors d'insertion ",e)
    def lire_conges(session):
        try:
            # requete pour lire toutes les lignes de la table congés
            resultats=session.query(conges).all()
            print("\n 📄 Liste des congés enregistrées :\n")
            for conge in resultats:
                print(f"ID:{conge.id},Employé:{conge.employe_id},"
                      f"Type_conge:{conge.type_conge},",
                      f"statut:{conge.statut}")
        except Exception as e:
            print("❌ Erreur lors de la lecture des données :", e)

# ============================================ filtrer les données ========================================

    def filtrer_conges(session,statut=None):
        try:
            requete=session.query(conges)
            if statut:
                requete=requete.filter(conges.statut==statut)
            resultats=requete.all()
            print("\n🔍 Résultats du filtre :\n")
            if not resultats:
                print("Aucune conge trouvée avec les critères donnés.")
            else:
                for conge in resultats:
                    print(f"- ID: {conge.id},"
                        f"Employé: {conge.employe_id},"
                        f" Type_conge: {conge.type_conge}, "
                        f"Début: {conge.date_debut},"
                        f"Fin: {conge.date_fin},"
                        f"Statut: {conge.statut}")
        except Exception as e:
            print("❌ Erreur lors du filtrage :", e)
    
except Exception as e:
    print("\n erreur d'insertion de données ")

# =================================== exmple d'insertion dans la table congés =================================

# liste_conges == > une liste de dictionnaires // chaque dictionnaire est une congés
liste_conges=[
    {
        'employe_id':14,
        'type_conge':'Congé maternité',
        'date_debut':'2024-01-01',
        'date_fin':'2024-04-29',
        'statut':'terminé'
    },
    { 
        'employe_id':53,
        'type_conge':'Congé annuel',
        'date_debut':'2025-08-01',
        'date_fin':'2025-08-15',
        'statut':'validé'
    },
    {
        'employe_id':173,
        'type_conge':'Congé maladie',
        'date_debut':'2025-05-20',
        'date_fin':'2025-06-03',
        'statut':'terminé'
    },
    {
        'employe_id':397,
        'type_conge':'Congé paternité',
        'date_debut':'2025-08-01',
        'date_fin':'2025-08-15',
        'statut':'en attente'
    }

]
# ajout des congés 
ajouter_conge(session,liste_conges)

# lecture des congés
lire_conges(session)

# Filtrer les congés "terminé" 
filtrer_conges(session,statut="terminé")
