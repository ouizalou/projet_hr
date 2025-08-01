# une bibliotheque qui permet de créer de l'interfaces  graphiques GUI - graphique User Interface 
import tkinter as tk
from tkinter import messagebox
from analyse_rh_mysql_pandas import (get_departements,get_employes_par_departement,get_nbr_embauches,
                                     engine, stats_employes_salaire, stats_departements, graphe_departement,
                             graphe_salaire, graphe_promotion, graphe_embauche, export_fichier)

# === 🎨 Couleurs modernes ===
BG_COLOR = "#f4f6f9"         # Fond clair doux
TITLE_COLOR = "#1f2937"      # Gris foncé pro
BTN_COLOR = "#2d89ef"        # Bleu principal
BTN_TEXT = "black"
QUIT_COLOR = "#e11d48"       # Rouge framboise doux
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 18, "bold")

# créer la fenetre principale 
root=tk.Tk()
#Titre de la fenêtre
root.title("Interface de Gestion RH: Statistiques et Graphiques ")
# Taille de la fenêtre.
root.geometry("")
# Changer le fond de la fenêtre
root.configure(bg=BG_COLOR)  # Bleu clair très doux

# Ajouter un titre en haut de l'interface
titre = tk.Label(root, text="📊 Tableau de Bord RH", font=TITLE_FONT, bg=BG_COLOR, fg=TITLE_COLOR)
titre.pack(pady=20)

# === 🗓️ Filtre par Année ===
anne_var=tk.StringVar(value="2025")
annees_disponibles=[str(a) for a in range(1987,2026)]
filtre_frame=tk.Frame(root,bg=BG_COLOR)
filtre_frame.pack(pady=5)
tk.Label(filtre_frame,text="Filtrer par année :", font=FONT, bg=BG_COLOR).pack(side=tk.LEFT, padx=5)
annee_menu=tk.OptionMenu(filtre_frame,anne_var,*annees_disponibles)
annee_menu.config(bg="white",font=("Segoe UI", 10), width=10)
annee_menu.pack(side=tk.LEFT)
# Label pour afficher le nombre d'embauches
embauche_label = tk.Label(root, text="", font=FONT, bg=BG_COLOR, fg=TITLE_COLOR)
embauche_label.pack(pady=5)

# === 🏢 Filtre par département ===
departement_var=tk.StringVar(value="Tous")
departements = ["Tous"] + get_departements(engine)
departement_frame=tk.Frame(root,bg=BG_COLOR)
departement_frame.pack(pady=5)
tk.Label(departement_frame, text="Filtrer par département :",font=FONT, bg=BG_COLOR).pack(side=tk.LEFT, padx=5)
departement_menu=tk.OptionMenu(departement_frame,departement_var,*departements)
departement_menu.config(bg="white",font=("Segoe UI", 10),width=20)
departement_menu.pack(side=tk.LEFT)

#  Créer un cadre (Frame) pour aligner les boutons au centre
frame=tk.Frame(root,bg=BG_COLOR)
frame.pack(expand=True)

# === 🔁 Barre de statut dynamique ===
statuts_var=tk.StringVar(value="✅ Prêt")
statuts_label=tk.Label(root, textvariable=statuts_var, bd=1, relief=tk.SUNKEN,anchor="w",bg=BG_COLOR,font=("Segoe UI", 10))
statuts_label.pack(side=tk.BOTTOM,fill=tk.X)




# === 🔄 Utilitaire avec statut ===
def exec_with_status(func, msg_success="✅ Action effectuée avec succès."):
    try:
        func(engine)
        statuts_var.set(msg_success)
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
        statuts_var.set("❌ Une erreur est survenue.")



frame.configure(bg=BG_COLOR)  # Même couleur que la fenêtre

def afficher_employes_par_departement():
    try:
        departement = departement_var.get()
        print(f"Département sélectionné : {departement}")  # Debugging

        if departement == "Tous":
            messagebox.showinfo("Info", "Veuillez sélectionner un département spécifique.")
            return

        # Récupérer les employés du département sélectionné
        df = get_employes_par_departement(engine, departement)
        print(f"DataFrame retourné : {df.head()}")  # Debugging

        if df.empty:
            messagebox.showinfo("Résultat", f"Aucun employé trouvé dans le département {departement}.")
            return

        # Nouvelle fenêtre popup
        fenetre = tk.Toplevel(root)
        fenetre.title(f"📋 Employés du département : {departement}")
        fenetre.geometry("1000x500")
        fenetre.configure(bg=BG_COLOR)

        # Ajouter un titre dans la fenêtre popup
        titre = tk.Label(fenetre, text=f"📋 Liste des employés - {departement}", font=TITLE_FONT, bg=BG_COLOR)
        titre.pack(pady=10)

        # Affichage du tableau des employés
        text_widget = tk.Text(fenetre, wrap="none", font=("Segoe UI", 10), height=20)
        text_widget.pack(fill="both", expand=True)

        # Affichage des colonnes
        colonnes = "\t\t".join(df.columns)
        text_widget.insert(tk.END, colonnes + "\n")
        text_widget.insert(tk.END, "-" * 150 + "\n")

        # Affichage des lignes des employés
        for index, row in df.iterrows():
            ligne = "\t\t".join(str(v) for v in row)
            text_widget.insert(tk.END, ligne + "\n")

        text_widget.config(state="disabled")  # Lecture seule

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")


def update_nombre_employee_embauche(*args):
    try:
        annee=anne_var.get()
        nombre_embauche=get_nbr_embauches(engine,annee)
        embauche_label.config(text=f"👥 {nombre_embauche} embauchees par {annee}")
        statuts_var.set(f"données mis à jour pour {annee}")
    except Exception as e:
        embauche_label.config(text="❌ Erreur lors du chargement.")
        statuts_var.set("❌ Une erreur est survenue.")
anne_var.trace_add("write", update_nombre_employee_embauche)



# Fonction pour exécuter l'analyse des employés
def on_stats_employees():
    try:
        stats_employes_salaire(engine)    # Appel de la fonction d'analyse des départements
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

# Fonction pour exécuter l'analyse des départements
def on_stats_departments():
    try:
        stats_departements(engine)  # Appel de la fonction d'analyse des départements
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

# Fonction pour afficher le graphique de répartition des employés par département
def on_graphe_department():
    try:
        graphe_departement(engine)  # Appel de la fonction de graphique des départements
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")



# Fonction pour afficher le graphique de répartition des employés par département
def on_graphe_salaire():
    try:
        graphe_salaire(engine)    # Appel de la fonction de graphique des salaires
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

# Fonction pour afficher le graphique des promotions et évolutions salariales
def on_graphe_promotion():
    try:
        graphe_promotion(engine)  # Appel de la fonction de graphique des promotions
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")


# Fonction pour afficher le graphique des promotions et évolutions salariales
def on_graphe_embauche():
    try:
        annee=anne_var.get()
        graphe_embauche(engine,annee=annee)
        statuts_var.set(f"📅 Embauches affichées pour {annee}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
        statuts_var.set("❌ Une erreur est survenue.")

# Fonction pour exporter les fichiers
def on_export_fichier():
    try:
        export_fichier(engine)
        messagebox.showinfo("Exportation réussie", "Les fichiers ont été exportés avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")


# Création des boutons alignés avec grid
buttons = [    
    ("📄 Liste Employés par Département", afficher_employes_par_departement),
    ("📊 Statistiques Salaires", on_stats_employees),
    ("📁 Données Départements", on_stats_departments),
    ("🏢 Répartition par Département", on_graphe_department),
    ("💼 Salaire Moyen par Poste", on_graphe_salaire),
    ("📈 Hausse Salaire Promotion", on_graphe_promotion),
    ("📅 Embauches par Année", on_graphe_embauche),
    ("⬇️ Exporter les Fichiers", on_export_fichier),

]

# command=on_stats_departments quand le bouton est cliqué, il appelle la fonction on_stats_departments(), 
# qui exécute l'analyse des salaires des employés.

for i, (text, command) in enumerate(buttons):
    tk.Button(frame, text=text, command=command, width=40, height=2,bg=BTN_COLOR,fg=BTN_TEXT,font=FONT,
              activebackground="#1e60b3",relief=tk.FLAT).grid(row=i, column=0, padx=20, pady=6)



# Bouton Quitter en dessous
tk.Button(frame, text="❌ Quitter", command=root.quit, width=20, height=2, bg=QUIT_COLOR,fg="black",font=FONT,
          relief=tk.FLAT,activebackground="#b91c1c").grid(row=len(buttons), column=0, padx=20, pady=10)


# ajouter un label en bas de la fenetre  bd -->  borderwidth relief --> le style de la border anchor --> aligne le texte
statuts_label=tk.Label(root, text="Prêt", bd=1,relief=tk.SUNKEN,anchor="w",bg="#f0f8ff")
# placer le label side --> placer le label a gauche, droite, haut, bas , fill --> horizontal, vertical 
statuts_label.pack(side=tk.BOTTOM, fill=tk.X)
statuts_label.config(text="Statistiques chargées avec succès ✅")


update_nombre_employee_embauche()
afficher_employes_par_departement()
# lancer l'interface 
root.mainloop()


