
# =====================================================================================
# 📊 SCRIPT : Analyse des données RH - Salaires, Départements, Promotions et Embauches
# 🗂️ Connexion à la base de données RH MySQL via SQLAlchemy
# 📈 Extraction, traitement et visualisation des données avec Pandas, Matplotlib et Seaborn
# 🖥️ Interface simple avec Tkinter pour afficher des messages d'information à l'utilisateur
# 💾 Export des résultats au format CSV/Excel et sauvegarde des graphiques
# =====================================================================================

import tkinter as tk
from tkinter import messagebox

# sqlalchemy pour gerer la connection a la base de donnees
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn
import os


try:
    import tkinter as tk
    from tkinter import messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


# informations de connexion MySQL
host='localhost'
port='3306'
DB_name='hr_sample'
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
#============== EMPLOYEES =============

    print(" \n 📊 les statistiques sur la colonne  salary : \n")
def stats_employees(engine):
    DF_employees=load_sql("SELECT * FROM employees",engine)
    # affiche les statistiques descriptives de la colonne 'salary'
    if TKINTER_AVAILABLE:
        messagebox.showinfo("Statistiques Salaires",DF_employees['salary'].describe().to_string())
    else:
        print("Statistiques Salaires:\n", DF_employees['salary'].describe())
    # afficher les premières lignes des données
    print("\n 📋 les données de la table employees :\n ")
    print(DF_employees.head())
 
stats_employees(engine)

# =========== DEPARTMENTS ================
print("\n 📋 les données de la table departments :\n ")
def stats_departments(engine):
    DF_departments=load_sql("SELECT *FROM departments",engine)
    print(DF_departments.head())
    # info() structure de DataFarme (nombre de ligneet colonne, noms des colonnes, 
    # les types de donnes les nombre de valeurs null par colonne, utilisation mémoire)
    print(" \n  🧠 la structure de datafarme :\n ")
    print(DF_departments.info())
    # Statistiques sur les colonnes numériques
    print(" \n 📈  les statistiques sur les colonnes numeriues: \n")
    print(DF_departments.describe())

stats_departments(engine)
 # ============ nombre d'emlpoyer par departement ===========

def graphe_department(engine):
    query="""SELECT d.department_name,count(d.department_id) AS nbr_employes
        FROM  employees e
        inner JOIN  departments d
        ON e.department_id =d.department_id
        GROUP BY d.department_name
        ORDER BY  nbr_employes DESC"""
    DF_emp_depart=load_sql(query,engine)
    print(" \n 👥📂 Répartition des employés par département :\n")
    print(DF_emp_depart.head())
    plt.close()
    print( "\n 📊 visualisation de  Nombre d'employés par département en bar :\n")
    plt.figure(figsize=(6,4))
    sbn.barplot(data=DF_emp_depart ,x='nbr_employes', y='department_name',palette="magma")
    plt.title("Nombre d'employés par département")
    plt.xlabel("Nombre d'employees")
    plt.ylabel("Département")
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR,"Nombre_d'employes_par_departement.png"))
    plt.show()

graphe_department(engine)
# ============= SALAIRE MOYEN PAR POSTE ================
print("💰 salaire moyen par poste :")
def graphe_salaire(engine):
    query=""" select j.job_title , ROUND(AVG(e.salary)) AS salaire_moyen
        FROM  employees e
        inner JOIN  jobs j 
        ON e.job_id  =j.job_id
        GROUP BY j.job_title
        ORDER BY salaire_moyen  desc """
    DF_salaire=load_sql(query,engine)
    print(DF_salaire.head())
    plt.close()
    plt.figure(figsize=(8,6))

    # palette= magma, deep, muted, pastel, colorblind,dark, bright,viridis, cividis, plasma, cool,BuPu, BuGn,
    sbn.barplot(data=DF_salaire, x="salaire_moyen",y="job_title", palette="bright")
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
    query=""" select p.employee_id,e.first_name ,e.last_name,p.old_salary,p.new_salary,
        (p.new_salary - p.old_salary) as augmentation,
        ROUND((p.new_salary - p.old_salary)/p.old_salary*100,2) as pourcentage
        FROM promotions p 
        inner JOIN  employees e 
        ON e.employee_id   =p.employee_id
        ORDER BY pourcentage  desc """
    DF_evolution_promo=load_sql(query,engine)
    print(DF_evolution_promo.head())
    plt.close()
    plt.figure(figsize=(8,6))
    sbn.barplot(data=DF_evolution_promo, x="pourcentage", y="first_name",palette="colorblind")
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
        query=F"""select YEAR(e.hire_date) as annee_embauche,count(*) as nombre_employee
            from employees e
            where YEAR(e.hire_date) ={annee}
            group by annee_embauche 
            order by annee_embauche """
    else:
        query = """
        SELECT YEAR(e.hire_date) AS annee_embauche, COUNT(*) AS nombre_employee
        FROM employees e
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
    DF_salaire=load_sql(""" select j.job_title , ROUND(AVG(e.salary)) AS salaire_moyen
        FROM  employees e
        inner JOIN  jobs j 
        ON e.job_id  =j.job_id
        GROUP BY j.job_title
        ORDER BY salaire_moyen  desc """,engine)
    plt.close()
    DF_employees=load_sql("SELECT * FROM employees",engine)
    DF_evolution_promo=load_sql(""" select p.employee_id,e.first_name ,e.last_name,p.old_salary,p.new_salary,
        (p.new_salary - p.old_salary) as augmentation,
        ROUND((p.new_salary - p.old_salary)/p.old_salary*100,2) as pourcentage
        FROM promotions p 
        inner JOIN  employees e 
        ON e.employee_id   =p.employee_id
        ORDER BY pourcentage  desc """,engine)
    DF_salaire.to_csv("salaire_moyen_par_poste.csv", index=False)
    DF_employees.to_excel("employes_par_departement.xlsx", index=False)
    DF_evolution_promo.to_csv("evolution_salaires_promotion.csv", index=False)

export_fichier(engine)

def get_nbr_embauches(engine, annee):
    query = f"""
        SELECT COUNT(*) AS nombre_employee
        FROM employees
        WHERE YEAR(hire_date) = {annee}
    """
    df_nombre_emp = load_sql(query, engine)
    return int(df_nombre_emp["nombre_employee"].iloc[0]) if not df_nombre_emp.empty else 0

def graphe_embauche_dep(engine, departement, annee=None):
    query = f"""
    SELECT YEAR(e.hire_date) AS annee_embauche, d.department_name, COUNT(*) AS nombre_employee
    FROM employees e
    INNER JOIN departments d ON e.department_id = d.department_id
    WHERE d.department_name = '{departement}'
    {"AND YEAR(e.hire_date) = " + str(annee) if annee else ""}
    GROUP BY YEAR(e.hire_date), d.department_name
    ORDER BY annee_embauche;
    """

    df = load_sql(query, engine)

    if df.empty:
        raise ValueError(f"Aucune donnée trouvée pour {departement} {f'en {annee}' if annee else ''}")

    plt.close()
    plt.figure(figsize=(8, 6))
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

def get_departements(engine):
    query = """
    SELECT DISTINCT d.department_name
    FROM employees e
    INNER JOIN departments d ON e.department_id = d.department_id
    ORDER BY d.department_name
    """
    df = load_sql(query, engine)
    return df["department_name"].tolist()

def get_employes_par_departement(engine, departement):
    try:
        # Requête SQL pour récupérer les employés d'un département spécifique
        query = f"""
        SELECT 
            YEAR(e.hire_date) AS annee, 
            d.department_id as id, 
            e.first_name, 
            e.last_name,
            j.job_title,
            e.salary ,
            e.retirement_status
        FROM employees e
        INNER JOIN departments d 
            ON e.department_id = d.department_id
        inner join jobs j on e.job_id =j.job_id
        WHERE d.department_name = '{departement}'  -- Filtre par le nom du département
        ORDER BY annee;
        """
        
        # Exécuter la requête SQL et obtenir le DataFrame
        df = pd.read_sql(query, engine)
        
        # Vérification si le DataFrame est vide
        if df.empty:
            print(f"Aucun employé trouvé pour le département {departement}.")
        return df
    except Exception as e:
        print(f"Erreur lors de la récupération des employés : {e}")
        return pd.DataFrame()  # Retourner une DataFrame vide en cas d'erreur



