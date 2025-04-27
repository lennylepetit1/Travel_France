import tkinter as tk
from tkinter import ttk
import pandas as pd
import re

# Charger le CSV
file_path = 'C:/Users/lenny/OneDrive/Documents/programmation projet/Fun_Project/TABLEAU FINALE.csv'
df = pd.read_csv(file_path, sep=';')

# Supprimer les espaces superflus dans les noms de colonnes et dans les valeurs
df.columns = df.columns.str.strip()
df['Départ'] = df['Départ'].str.strip()
df['Arrivée'] = df['Arrivée'].str.strip()

# Convertir la colonne 'Date de départ' en format datetime pour un meilleur filtrage
df['Date de départ'] = pd.to_datetime(df['Date de départ'], format='%d/%m/%Y', errors='coerce')

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



# Variables globales pour garder le contexte
destination_en_attente = None
date_en_attente = None

# Fonction chatbot corrigée avec gestion de contexte
def chatbot_response(question):
    global destination_en_attente
    global date_en_attente

    question = question.lower()

    # Chercher une date dans la question
    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', question)
    date_filter = None
    if date_match:
        try:
            date_filter = pd.to_datetime(date_match.group(1), format='%d/%m/%Y')
        except Exception as e:
            print(f"Erreur de parsing de la date : {e}")

    # Vérifier si on attend la ville de départ
    if destination_en_attente is not None:
        # On attend que l'utilisateur donne sa ville de départ
        depart_trouve = None
        for ville in df['Départ'].unique().tolist():
            if ville.lower() in question:
                depart_trouve = ville
                break

        if depart_trouve:
            # Sauvegarder la destination avant de reset
            destination = destination_en_attente

            # Reset du contexte
            destination_en_attente = None
            date_en_attente = None

            # Chercher les trajets
            filtered_data = df[(df['Départ'] == depart_trouve) & (df['Arrivée'] == destination)]

            if not filtered_data.empty:
                response = f"Voici les trajets disponibles de {depart_trouve} à {destination} :\n"
                for _, row in filtered_data.iterrows():
                    response += f"- {row['Transport']} : {row['Durée']} | Prix : {row['Prix']}\n"
                return response
            else:
                return f"Désolé, aucun trajet trouvé de {depart_trouve} à {destination}."
        else:
            return "Je n'ai pas compris ta ville de départ. Peux-tu réessayer en précisant ta ville de départ ?"

    # Sinon, comportement normal
    villes_trouvees = []

    for ville in df['Départ'].unique().tolist() + df['Arrivée'].unique().tolist():
        if ville.lower() in question and ville not in villes_trouvees:
            villes_trouvees.append(ville)

    if len(villes_trouvees) >= 2:
        depart_trouve, arrivee_trouvee = villes_trouvees[0], villes_trouvees[1]

        filtered_data = df[(df['Départ'] == depart_trouve) & (df['Arrivée'] == arrivee_trouvee)]

        if date_filter is not None:
            filtered_data = filtered_data[filtered_data['Date de départ'] == date_filter]

        if not filtered_data.empty:
            response = f"Voici les trajets disponibles de {depart_trouve} à {arrivee_trouvee}"
            if date_filter is not None:
                response += f" le {date_filter.strftime('%d/%m/%Y')}"
            response += " :\n"
            for _, row in filtered_data.iterrows():
                response += f"- {row['Transport']} : {row['Durée']} | Prix : {row['Prix']}\n"
            return response
        else:
            return f"Je n'ai pas d'informations sur ce trajet entre {depart_trouve} et {arrivee_trouvee}" + (f" pour le {date_filter.strftime('%d/%m/%Y')}" if date_filter else "") + "."

    elif len(villes_trouvees) == 1:
        # Une seule ville détectée -> demander la ville de départ
        destination_en_attente = villes_trouvees[0]
        if date_filter is not None:
            date_en_attente = date_filter
        return f"Tu veux aller à {destination_en_attente} ? Bonne idée, mais peux-tu préciser ta ville de départ ? "

    else:
        return "Désolé, je n'ai pas compris. Essaie de poser une question sur les trajets entre deux villes."


# Fonction pour afficher les réponses du chatbot
def on_send():
    user_input = user_entry.get()
    chat_log.config(state=tk.NORMAL)  # Rendre le chat log modifiable pour afficher la réponse
    chat_log.insert(tk.END, "Vous: " + user_input + "\n")
    
    # Obtenir la réponse du chatbot
    bot_reply = chatbot_response(user_input)
    chat_log.insert(tk.END, "Bot: " + bot_reply + "\n\n")
    
    # Faire défiler la fenêtre vers le bas pour afficher la dernière réponse
    chat_log.yview(tk.END)

    # Effacer le champ de saisie de l'utilisateur
    user_entry.delete(0, tk.END)
    
    chat_log.config(state=tk.DISABLED)  # Revenir à un état non modifiable après l'insertion

# Créer la fenêtre principale
root = tk.Tk()
root.title("Filtre de Trajets et Chatbot")

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

# Interface de chatbot
tk.Label(root, text="Chatbot").grid(row=5, column=0, columnspan=2)
chat_log = tk.Text(root, height=15, width=60, state=tk.DISABLED)
chat_log.grid(row=6, column=0, columnspan=2)
user_entry = tk.Entry(root, width=50)
user_entry.grid(row=7, column=0, columnspan=2)
send_button = tk.Button(root, text="Envoyer", command=on_send)
send_button.grid(row=8, column=0, columnspan=2)

# Lancer l'application
root.mainloop()
