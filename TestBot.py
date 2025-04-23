import tkinter as tk
from tkinter import ttk

# Informations sur les trajets (très simple, pour une démonstration)
trajets = {
    "Paris": {
        "Marseille": "Train TGV : 3h15, Bus : 10h, Voiture : 7h",
        "Lyon": "Train TGV : 2h, Bus : 6h, Voiture : 5h"
    },
    "Marseille": {
        "Paris": "Train TGV : 3h15, Bus : 10h, Voiture : 7h",
        "Lyon": "Train : 1h40, Bus : 5h, Voiture : 3h"
    },
    "Lyon": {
        "Paris": "Train TGV : 2h, Bus : 6h, Voiture : 5h",
        "Marseille": "Train : 1h40, Bus : 5h, Voiture : 3h"
    },
    "Toulouse": {
        "Bordeaux": "Train : 2h, Bus : 4h, Voiture : 3h30",
        "Paris": "Train : 4h30, Avion : 1h20"
    },
    "Nice": {
        "Marseille": "Train : 2h30, Bus : 3h, Voiture : 2h30",
        "Paris": "Train TGV : 5h30, Avion : 1h30"
    },
    "Nantes": {
        "Bordeaux": "Train : 3h, Bus : 6h, Voiture : 4h",
        "Paris": "Train : 2h, Bus : 4h, Voiture : 3h"
    },
    "Montpellier": {
        "Strasbourg": "Train : 5h30, Avion : 1h30",
        "Paris": "Train : 3h, Avion : 1h10"
    },
    "Strasbourg": {
        "Paris": "Train : 2h30, Avion : 1h15",
        "Montpellier": "Train : 5h30, Avion : 1h30"
    },
    "Bordeaux": {
        "Paris": "Train : 3h, Avion : 1h10",
        "Nice": "Train : 8h, Voiture : 9h"
    },
    "Lille": {
        "Paris": "Train : 1h, Bus : 2h, Voiture : 2h",
        "Strasbourg": "Train : 3h30, Avion : 1h"
    }
}

# Fonction pour obtenir la réponse du chatbot
def chatbot_response(question):
    # Liste des villes connues
    villes = list(trajets.keys())

    # Convertir la question en minuscules pour éviter les problèmes de casse
    question = question.lower()

    # Rechercher les villes dans la question
    villes_trouvees = []
    for ville1 in villes:
        for ville2 in villes:
            # Vérifier si les deux villes sont mentionnées dans la question
            if ville1.lower() in question and ville2.lower() in question and ville1 != ville2:
                villes_trouvees.append((ville1, ville2))

    # Si des villes sont trouvées, donner la réponse correspondante
    if villes_trouvees:
        ville1, ville2 = villes_trouvees[0]
        if ville2 in trajets.get(ville1, {}):
            return f"Trajet {ville1} → {ville2} : {trajets[ville1][ville2]}"
        else:
            return f"Je n'ai pas d'informations sur ce trajet entre {ville1} et {ville2}."
    
    # Si aucune correspondance n'est trouvée
    return "Désolé, je n'ai pas compris. Essaye de poser une question sur les trajets entre deux villes."

# Création de l'interface Tkinter
def start_chat():
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

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Chatbot Transport")

    # Zone de texte pour afficher la conversation
    chat_log = tk.Text(root, height=15, width=60, state=tk.DISABLED)
    chat_log.grid(row=0, column=0, columnspan=2)

    # Champ de saisie de l'utilisateur
    user_entry = tk.Entry(root, width=60)
    user_entry.grid(row=1, column=0)

    # Bouton pour envoyer un message
    send_button = tk.Button(root, text="Envoyer", command=on_send)
    send_button.grid(row=1, column=1)

    # Lancer l'application
    root.mainloop()

# Démarrer l'interface graphique
start_chat()
