import tkinter as tk
from tkinter import ttk
import pandas as pd

# Charger le CSV
file_path = 'C:/Users/lenny/OneDrive/Documents/programmation projet/Fun_Project/TABLEAU FINALE.csv'
df = pd.read_csv(file_path, sep=';')

# Supprimer les espaces superflus dans les noms de colonnes et dans les valeurs
df.columns = df.columns.str.strip()
df['Départ'] = df['Départ'].str.strip()
df['Arrivée'] = df['Arrivée'].str.strip()

# Convertir la colonne 'Date de départ' en format datetime pour un meilleur filtrage
df['Date de départ'] = pd.to_datetime(df['Date de départ'], format='%d/%m/%Y', errors='coerce')

# Afficher les noms de colonnes pour vérifier
print("Colonnes disponibles dans le fichier CSV :", df.columns)

# Fonction pour filtrer et afficher les trajets
def afficher_trajets():
    depart = depart_combobox.get()
    arrivee = arrivee_combobox.get()
    date = date_combobox.get()

    print(f"Filtrage avec les valeurs: Départ: {depart}, Arrivée: {arrivee}, Date: {date}")

    # Convertir la date choisie en format datetime pour le filtrage
    try:
        date = pd.to_datetime(date, format='%d/%m/%Y')
    except Exception as e:
        print(f"Erreur de conversion de la date : {e}")
        return

    print(f"Date après conversion : {date}")

    # Filtrer les données
    filtered_data = df[(df['Départ'] == depart) & (df['Arrivée'] == arrivee) & (df['Date de départ'] == date)]

    print(f"Résultats du filtrage : {filtered_data.shape[0]} trajets trouvés")

    # Afficher les résultats
    for row in tree.get_children():
        tree.delete(row)

    if filtered_data.empty:
        tree.insert("", "end", values=("Aucun trajet disponible", "", "", "", "", ""))
    else:
        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=(row['Départ'], row['Arrivée'], row['Date de départ'].strftime('%d/%m/%Y'),
                                          row['Durée'], row['Transport'], row['Prix']))

# Créer la fenêtre principale
root = tk.Tk()
root.title("Filtre de Trajets")

# Créer les combobox pour les lieux de départ et d'arrivée
tk.Label(root, text="Lieu de départ").grid(row=0, column=0)
depart_combobox = ttk.Combobox(root, values=df['Départ'].unique().tolist())
depart_combobox.grid(row=0, column=1)

tk.Label(root, text="Lieu d'arrivée").grid(row=1, column=0)
arrivee_combobox = ttk.Combobox(root, values=df['Arrivée'].unique().tolist())
arrivee_combobox.grid(row=1, column=1)

# Créer un champ pour sélectionner la date
tk.Label(root, text="Date de départ (jj/mm/aaaa)").grid(row=2, column=0)
date_combobox = ttk.Combobox(root, values=df['Date de départ'].dt.strftime('%d/%m/%Y').unique().tolist())
date_combobox.grid(row=2, column=1)

# Bouton pour afficher les trajets
btn_filter = tk.Button(root, text="Afficher les trajets", command=afficher_trajets)
btn_filter.grid(row=3, column=0, columnspan=2)

# Créer un tableau pour afficher les résultats
columns = ('Départ', 'Arrivée', 'Date de départ', 'Durée', 'Transport', 'Prix')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)

tree.grid(row=4, column=0, columnspan=2)

# Lancer l'application
root.mainloop()
