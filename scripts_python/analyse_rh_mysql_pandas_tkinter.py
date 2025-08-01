import tkinter as tk
from tkinter import messagebox

# sqlalchemy pour gerer la connection a la base de donnees
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn
import os

import subprocess
import sys

# informations de connexion MySQL
host='localhost'
port='3306'
DB_name='sample_rh'
username='root'
password='root'

# creer une URL de connexion pour MySQL
connection_string=f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{DB_name}'

# Style général
sbn.set(style="whitegrid")

# Dossier pour sauvegarder les graphes
GRAPH_DIR='graphs_hr'
os.makedirs(GRAPH_DIR,exist_ok=True)

# créer la connexion avec SQLalchemy
try:
    engine=create_engine(connection_string)
except Exception as e:
    print(" ❌ Erreur lors de la connexion  :", e)

# Fonction utilitaire pour charger une requête SQL
def load_sql(query,engine):
    try:
        return pd.read_sql(query,engine)
    except Exception as e:
        print("❌ Erreur  de la requête sql :", e)


# Charger des données avec une requête SQL dans un DataFrame pandas
#============== EMPLOYES =============

    print(" \n 📊 les statistiques sur la colonne  salaire_net : \n")
def stats_employes_salaire(engine):
    DF_salaires=load_sql("SELECT * FROM salaires",engine)
    # affiche les statistiques descriptives de la colonne 'salaire_net'
    messagebox.showinfo("Statistiques Salaires",DF_salaires['salaire_net'].describe().to_string())
    # afficher les premières lignes des données
    print("\n 📋 les données de la table salaires :\n ")
    print(DF_salaires.head())
 
stats_employes_salaire(engine)

# =========== DEPARTeMENTS ================
print("\n 📋 les données de la table departements :\n ")
def stats_departements(engine):
    DF_departements=load_sql("SELECT *FROM departements",engine)
    print(DF_departements.head())
    # info() structure de DataFarme (nombre de ligneet colonne, noms des colonnes, 
    # les types de donnes les nombre de valeurs null par colonne, utilisation mémoire)
    print(" \n  🧠 la structure de datafarme :\n ")
    print(DF_departements.info())
    # Statistiques sur les colonnes numériques
    print(" \n 📈  les statistiques sur les colonnes numeriques: \n")
    print(DF_departements.describe())

stats_departements(engine)
 # ============ nombre d'empoyer par departement ===========

def graphe_departement(engine):
    query="""SELECT d.nom,count(d.id) AS nbr_employes
        FROM  employes e
        inner JOIN  departements d
        ON e.departement_id =d.id
        GROUP BY d.nom
        ORDER BY  nbr_employes DESC"""
    DF_emp_depart=load_sql(query,engine)
    print(" \n 👥📂 Répartition des employés par département :\n")
    print(DF_emp_depart.head())
    plt.close()
    print( "\n 📊 visualisation de  Nombre d'employés par département en bar :\n")
    plt.figure(figsize=(6,4))
    sbn.barplot(data=DF_emp_depart ,x='nbr_employes', y='nom',palette="magma")
    plt.title("Nombre d'employés par département")
    plt.xlabel("Nombre d'employees")
    plt.ylabel("Département")
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR,"Nombre_d'employes_par_departement.png"))
    plt.show()

graphe_departement(engine)
# ============= SALAIRE MOYEN PAR POSTE ================
print("💰 salaire moyen par poste :")
def graphe_salaire(engine):
    query=""" select p.id as poste_id,p.intitule , ROUND(AVG(s.salaire_net)) AS salaire_moyen
        FROM  employes e
        inner JOIN  postes p ON e.poste_id  =p.id
        inner join salaires s on s.employe_id=e.id
        GROUP BY p.id,p.intitule
        ORDER BY salaire_moyen  desc"""
    DF_salaire=load_sql(query,engine)
    print(DF_salaire.head())
    plt.close()
    plt.figure(figsize=(12,16))

    # palette= magma, deep, muted, pastel, colorblind,dark, bright,viridis, cividis, plasma, cool,BuPu, BuGn,
    sbn.barplot(data=DF_salaire, x="salaire_moyen",y="intitule", palette="magma")
    plt.title("salaire moyen par poste")
    plt.xlabel("salaire moyen ")
    plt.ylabel("Poste")
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR,"Salaire_moyen_par_poste.png"))
    plt.show()

graphe_salaire(engine)
# =========== EVOLUTION SALAIRE APRES PROMOTION =============
print("\n 🔄 Evolution de salaire après promotion :\n")
def graphe_promotion(engine):
    query=""" select pr.employe_id,e.nom ,e.prenom,s.salaire_net,pr.nouveau_salaire,
        (pr.nouveau_salaire - s.salaire_net) as augmentation,
        ROUND((pr.nouveau_salaire - s.salaire_net)/s.salaire_net*100,2) as pourcentage
        FROM promotions pr 
        inner JOIN  employes e 
        ON e.id   =pr.employe_id
        inner join salaires s on s.employe_id=e.id
        ORDER BY pourcentage  desc ; """
    DF_evolution_promo=load_sql(query,engine)
    print(DF_evolution_promo.head())
    plt.close()
    plt.figure(figsize=(12,10))
    sbn.barplot(data=DF_evolution_promo, x="pourcentage", y="nom",palette="magma")
    plt.title("Top hausses de salaire après promotion ")
    plt.xlabel(" Augmentation")
    plt.ylabel("Employé")
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR,"Top_Hausse_de_salaire_après_promotion.png"))
    plt.show()

graphe_promotion(engine)
# ============== EMPLOYÉS EMBAUCHÉS PAR ANNÉE =================

print("\n 📆 nombre d'employees embaucher par annee :\n")
def graphe_embauche(engine,annee=None):
    if annee:
        query=F"""select YEAR(e.date_embauche) as annee_embauche,count(*) as nombre_employee
            from employes e
            where YEAR(e.date_embauche) ={annee}
            group by annee_embauche 
            order by annee_embauche """
    else:
        query = """
        SELECT YEAR(e.date_embauche) AS annee_embauche, COUNT(*) AS nombre_employee
        FROM employes e
        GROUP BY annee_embauche
        ORDER BY annee_embauche
        """

    DF_emp_embauch_an=load_sql(query,engine)
    print(DF_emp_embauch_an.head())
    plt.close()
    plt.figure(figsize=(8,6))
    # marker= o, s, ^, v, D, *, x, +
    sbn.lineplot(data=DF_emp_embauch_an,x="annee_embauche", y="nombre_employee",marker="D",color="blue")
    plt.title(" nombre d'employees embaucher par annee ")
    plt.xlabel(" Année embauche ")
    plt.ylabel(" Nombre d'employées ")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(GRAPH_DIR,"Nombre_employees_embaucher_par_annee.png"))

graphe_embauche(engine,annee=None)
# ================ Export des résultats CSV ==============
def export_fichier(engine):
    DF_salaire=load_sql(""" select p.intitule , ROUND(AVG(s.salaire_net)) AS salaire_moyen
        FROM  employes e
        inner JOIN  postes p
        ON e.poste_id  =p.id
        inner join salaires s on s.employe_id=e.id
        GROUP BY p.intitule """,engine)
    plt.close()
    DF_employees=load_sql("SELECT * FROM employes",engine)
    DF_evolution_promo=load_sql(""" select pr.employe_id,e.nom ,e.prenom,s.salaire_net,pr.nouveau_salaire,
        (pr.nouveau_salaire - s.salaire_net) as augmentation,
        ROUND((pr.nouveau_salaire - s.salaire_net)/s.salaire_net*100,2) as pourcentage
        FROM promotions pr 
        inner JOIN  employes e 
        ON e.id   =pr.employe_id
        inner join salaires s on s.employe_id=e.id
        ORDER BY pourcentage  desc """,engine)
    DF_salaire.to_csv("salaire_moyen_par_poste.csv", index=False)
    DF_employees.to_excel("employes_par_departement.xlsx", index=False)
    DF_evolution_promo.to_csv("evolution_salaires_promotion.csv", index=False)

export_fichier(engine)

def get_nbr_embauches(engine, annee):
    query = f"""
        SELECT COUNT(*) AS nombre_employee
        FROM employes
        WHERE YEAR(date_embauche) = {annee}
    """
    df_nombre_emp = load_sql(query, engine)
    return int(df_nombre_emp["nombre_employee"].iloc[0]) if not df_nombre_emp.empty else 0

get_nbr_embauches(engine,1994)
def graphe_embauche_dep(engine, departement, annee=None):
    query = f"""
    SELECT YEAR(e.date_embauche) AS annee_embauche, d.nom as nom_departement, COUNT(*) AS nombre_employee
    FROM employes e
    INNER JOIN departements d ON e.departement_id = d.id
    WHERE d.nom = '{departement}'
    {"AND YEAR(e.date_embauche) = " + str(annee) if annee else ""}
    GROUP BY YEAR(e.date_embauche), d.nom
    ORDER BY annee_embauche;
    """

    df = load_sql(query, engine)

    if df.empty:
        raise ValueError(f"Aucune donnée trouvée pour {departement} {f'en {annee}' if annee else ''}")

    plt.close()
    plt.figure(figsize=(10, 8))
    sbn.barplot(data=df, x="annee_embauche", y="nombre_employee", color="skyblue")

    titre = f"📊 Nombre d'employés embauchés - {departement}"
    if annee:
        titre += f" en {annee}"

    plt.title(titre)
    plt.xlabel("Année d'embauche")
    plt.ylabel("Nombre d'employés")
    plt.grid(True)
    plt.tight_layout()

    plt.show()
    plt.savefig(os.path.join(GRAPH_DIR, f"embauche_{departement}_{annee if annee else 'all'}.png"))
graphe_embauche_dep(engine,"Seize visionary web services" ,annee=None)
def get_departements(engine):
    query = """
    SELECT DISTINCT d.nom
    FROM employes e
    INNER JOIN departements d ON e.departement_id = d.id
    ORDER BY d.nom
    """
    df = load_sql(query, engine)
    return df["nom"].tolist()
get_departements(engine)
def get_employes_par_departement(engine, departement):
    try:
        # Requête SQL pour récupérer les employés d'un département spécifique
        query = f"""
        SELECT 
            YEAR(e.date_embauche) AS annee, 
            d.id as departement_id , 
            d.nom as nom_departement,
            e.nom as nom_employe, 
            e.prenom,
            p.intitule,
            e.statut_retraite
        FROM employes e
        INNER JOIN departements d 
            ON e.departement_id = d.id
        inner join postes p on e.poste_id =p.id
        WHERE d.nom = '{departement}'  
        ORDER BY annee;
        """
        
        # Exécuter la requête SQL et obtenir le DataFrame
        df = pd.read_sql(query, engine)
        print(df.head())
        # Vérification si le DataFrame est vide
        if df.empty:
            print(f"Aucun employé trouvé pour le département {departement}.")
        return df
    except Exception as e:
        print(f"Erreur lors de la récupération des employés : {e}")
        return pd.DataFrame()  # Retourner une DataFrame vide en cas d'erreur
get_employes_par_departement(engine,"Seize visionary web services")



