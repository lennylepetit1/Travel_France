import discord
import pandas as pd
import re
import os
from dotenv import load_dotenv
from discord.ext import commands

# Charger les variables d'environnement (.env)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Charger le CSV
file_path = 'C:\Users\dalia\OneDrive\Bureau\Bot'
df = pd.read_csv(file_path, sep=';')

# Nettoyer les données
df.columns = df.columns.str.strip()
df['Départ'] = df['Départ'].str.strip()
df['Arrivée'] = df['Arrivée'].str.strip()
df['Date de départ'] = pd.to_datetime(df['Date de départ'], format='%d/%m/%Y', errors='coerce')

# Variables pour le contexte du chatbot
destination_en_attente = None
date_en_attente = None

# Fonction du chatbot
def chatbot_response(question):
    global destination_en_attente
    global date_en_attente

    question = question.lower()

    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', question)
    date_filter = None
    if date_match:
        try:
            date_filter = pd.to_datetime(date_match.group(1), format='%d/%m/%Y')
        except Exception as e:
            print(f"Erreur de parsing de la date : {e}")

    if destination_en_attente is not None:
        depart_trouve = None
        for ville in df['Départ'].unique().tolist():
            if ville.lower() in question:
                depart_trouve = ville
                break

        if depart_trouve:
            destination = destination_en_attente
            destination_en_attente = None
            date_en_attente = None

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
        destination_en_attente = villes_trouvees[0]
        if date_filter is not None:
            date_en_attente = date_filter
        return f"Tu veux aller à {destination_en_attente} ? Bonne idée, mais peux-tu préciser ta ville de départ ? 😊"

    else:
        return "Désolé, je n'ai pas compris. Essaie de poser une question sur les trajets entre deux villes."

# Création du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore les messages du bot lui-même

    user_question = message.content

    # Utiliser la fonction chatbot
    response = chatbot_response(user_question)

    await message.channel.send(response)

# Lancer le bot
bot.run(TOKEN)
