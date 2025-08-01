
# =====================================================================================
# 📊 SCRIPT : Analyse et Prédiction des Salaires des Employés
# 🎯 OBJECTIF : 
#     - Se connecter à la base de données RH MySQL 🗄️
#     - Extraire et analyser les données des employés 👥
#     - Calculer des statistiques sur les salaires 💰 et l'ancienneté ⏳
#     - Utiliser des modèles de machine learning 🤖 (régression linéaire, RandomForest, SVM)
#       pour prédire les salaires et classifier les hauts salaires 📈
# 🛠️ OUTILS : Pandas, NumPy, SQLAlchemy, Scikit-learn, Seaborn, Matplotlib
# =====================================================================================


# =====================================================================================
# 📊 SCRIPT : Analyse et Prédiction des Salaires des Employés
# 🎯 OBJECTIF : 
#     - Se connecter à la base de données RH MySQL 🗄️
#     - Extraire et analyser les données des employés 👥
#     - Calculer des statistiques sur les salaires 💰 et l'ancienneté ⏳
#     - Utiliser des modèles de machine learning 🤖 (régression linéaire, RandomForest, SVM)
#       pour prédire les salaires et classifier les hauts salaires 📈
# 🛠️ OUTILS : Pandas, NumPy, SQLAlchemy, Scikit-learn, Seaborn, Matplotlib
# =====================================================================================


# ===============================          Faire des analyses statistiques (avec NumPy)        ===============
import pandas as pd
from sqlalchemy import create_engine

# numpy ==> permet de manipuler des tableaux multidimensionnels de manière rapide et efficace, ainsi que d'effectuer 
# des opérations mathématiques avancées
import numpy as np
import pymysql

# scikit learn est fournit des outils simples et efficaces pour l'analyses prédictive de données et de machine learning supérvisé 
# et non supérvisé
# modèle de machine learning de type régression lineaire
from sklearn.linear_model import LinearRegression

# train_test_split permet de diviser un jeu de données en deux parties ==> (jeu d'entrainnement(train:X_train==> x: les données ) :pour entrainer le modele /
#  jeu de test(test : y_test==> y: les etiquettes /cibles) :pour evaluer les performance de modele)
from sklearn.model_selection import train_test_split

import seaborn as sns
import matplotlib.pyplot as plt

# modéle d'apprentissage automatique supervisé de type classification
from sklearn.ensemble import RandomForestClassifier
# sert a évaluer les performance d'un modele de classification
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.svm import SVC

import joblib


# connexion a la base de données Mysql

try:
    engine=create_engine(f'mysql+pymysql://root:root@localhost:3306/hr_sample')
    connection=engine.connect()
    print("\n ✅  la connexion est bien réussie a la base de données")

    # requete sql avec jointures :employe+ jobs+ departement
    query="""select e.id,
	e.date_embauche,
	s.salaire_net,
	p.intitule,
	p.salaire_min,
	p.salaire_max,
	d.nom
	from employes e
	join postes p on e.poste_id=p.id
	join departements d on e.departement_id=d.id
    join salaires s on s.employe_id=e.id"""
    

    # lecture des données de la table employées
    DF_employees=pd.read_sql(query,engine)
    print(DF_employees.head())

    # convertir les hire_date en format datetime
    DF_employees['date_embauche']=pd.to_datetime(DF_employees['date_embauche'])
    # trie les données de ala table employées selon les date d'embauche 
    DF_employees=DF_employees.sort_values(by='date_embauche')
    print(DF_employees.head())

# =====================         Statistiques et calculs avec NumPy         ========================================

    salaires=DF_employees['salaire_net'].values
    print(" Salaire moyen:",np.mean(salaires))
    print("Salaire médian:",np.median(salaires))
    print("Ecart-type",np.std(salaires))

# ================================       Machine Learning avec Scikit-learn      ==================================

    # ======================      prédire les salaires selon les années d'anciénnté =====================
    #créer la variable anciennté
    DF_employees['anciennte']=(pd.to_datetime('today') - DF_employees['date_embauche']).dt.days / 365

    # suppression des lignes manquantes
    DF_employees.dropna(inplace=True)
    print(DF_employees.head())

    # définir les variables x et y
    # x : est la caractéristique d’entrée ==> ancienté
    x=DF_employees[['anciennte']]
    # y: la valeur a prédire ==> salaire
    y=DF_employees['salaire_net']

    # diviser les données en train(80% )/ test (20%)
    #random_state=42 : pour garantir des résultats reproductibles.
    x_train, x_test,y_train,y_test=train_test_split(x,y,test_size=0.2, random_state=42)

    # créer le modele de machine learning est LinearRegression
    modele=LinearRegression()

    # entrainner le modele avec les données d'entainement
    modele.fit(x_train,y_train)

    # evaluation de modele  ==> Affiche le score R² (coefficient de détermination) :R² = 1 : prédiction parfaite // 
    # R² = 0 : le modèle ne fait pas mieux qu'une moyenne // R² < 0 : le modèle est pire qu'une moyenne
    print("score R2:",modele.score(x_test,y_test))

    # tracer le graphe de relation entre les salaires et l'anciennté
    sns.scatterplot(data=DF_employees, x='anciennte',y='salaire_net')
    plt.title("Anciennté vs les salaires")
    plt.show()
    
    # ====>>> scrore R2 <0 les modele est pire que prédire  la moyenne ( la relation est trés faibles entre salaire et anciennte)
    # ==========================       Prédire si un nouvel employe est susceptible d'avoir un haut salaire     =========================
    
    print("\n prediction si un nouvel employe peut avoir un salaire haut :\n")
    # creation des variable cible
    DF_employees['haut_salaire']=(DF_employees['salaire_net']>9000).astype(int)

    # convertir les colonnes contenant de texte en categories puis en valeurs numerique avec cat.codes
    DF_employees['intitule']=DF_employees['intitule'].astype('category')
    DF_employees['intitule']=DF_employees['job_title'].cat.codes
    DF_employees['nom']=DF_employees['nom'].astype('category').cat.codes

    # definition des variables d'entrees / cibles
    x=DF_employees[['anciennte','salaire_min','salaire_max','intitule','nom']]
    y=DF_employees['haut_salaire']

    # separer les donees en train/test
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2, random_state=42)

    # creation et entrainement de modele 
    modele_classif=RandomForestClassifier(random_state=42)
    modele_classif.fit(x_train,y_train)
    print("\n🧾 Rapport de classification :\n")
    # prediction et evaluation 
    y_prediction=modele_classif.predict(x_test)
    print(classification_report(y_test,y_prediction))

    print("\n  Matrice de confusion modele classification randomForest \n")
    matrice_confusion=confusion_matrix(y_test,y_prediction)

    sns.heatmap(matrice_confusion,annot=True, fmt='d',cmap='Blues',
                xticklabels=['Pas haut salaire','Haut salaire'], yticklabels=['Pas haut salaire','Haut salaire'])
    plt.xlabel("Prédit")
    plt.ylabel("Réel")
    plt.title("Matrice de confusion")
    plt.show()
    # ======================      SVM : prédire haut salaire         ======================================
    # les variables d'entree /cible
    x=DF_employees[['anciennte','salaire_min','salaire_max','intitule','nom']]
    y=DF_employees[['haut_salaire']]

    # separer les variables train/test
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2, random_state=42)

    # creation de modele svm avec un noyau RBF par defaut
    svm_modele=SVC(kernel='rbf',C=1,gamma='scale')
    svm_modele.fit(x_train,y_train)

    # prediction
    y_prediction_svm = svm_modele.predict(x_test)

    # evaluation 
    print("\n🧾 Rapport de classification :\n")
    print(classification_report(y_test,y_prediction_svm))

    print("\n Matrice de confusion modele SVM \n")
    matrice_confusion=confusion_matrix(y_test,y_prediction)

    sns.heatmap(matrice_confusion,annot=True, fmt='d',cmap='Blues',
                xticklabels=['Pas haut salaire','Haut salaire'], yticklabels=['Pas haut salaire','Haut salaire'])
    plt.xlabel("Prédit")
    plt.ylabel("Réel")
    plt.title("Matrice de confusion")
    plt.show()

except Exception as e:
    print("\n❌ error lors de la connexion a la base de données ")
    print (e)
DF_employees.to_csv('employees_with_predictions.csv', index=False)


# Sauvegarder le modèle RandomForestClassifier entraîné
#joblib.dump(modele_classif, 'C:/Users/Admin/modele_haut_salaire.pkl',compress=3, protocol=4)
with open("modele_haut_salaire.pkl", "wb") as f:
    joblib.dump(modele_classif, f, protocol=4)
print("✅ Modèle RandomForest sauvegardé dans 'modele_haut_salaire.pkl'")



