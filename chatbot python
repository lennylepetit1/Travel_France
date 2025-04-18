import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import difflib
import unicodedata
import re
import pandas as pd


load_dotenv()

print("Lancement du bot...")

# Création de l'instance du client avec les intents appropriés
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot allumé !")
    # Synchroniser les commandes slash
    try:
        # sync
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Une erreur est survenue lors de la synchronisation des commandes : {e}")


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste des villes connues
villes_connues = [ "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Montpellier", "Strasbourg", 
    "Bordeaux", "Lille", "Rennes", "Toulon", "Reims", "Saint-Étienne", "Le Havre", "Villeurbanne", 
    "Dijon", "Angers", "Grenoble", "Saint-Denis", "Nîmes", "Aix-en-Provence", "Clermont-Ferrand", 
    "Le Mans", "Brest", "Tours", "Amiens", "Annecy", "Limoges", "Metz", "Perpignan", "Boulogne-Billancourt", 
    "Besançon", "Orléans", "Rouen", "Saint-Denis", "Montreuil", "Caen", "Argenteuil", "Saint-Paul", "Mulhouse", 
    "Nancy", "Roubaix", "Tourcoing", "Nanterre", "Vitry-sur-Seine", "Créteil", "Avignon", "Asnières-sur-Seine", 
    "Colombes", "Aubervilliers", "Poitiers", "Dunkerque", "Aulnay-sous-Bois", "Saint-Pierre", "Versailles", 
    "Le Tampon", "Courbevoie", "Rueil-Malmaison", "Béziers", "La Rochelle", "Pau", "Champigny-sur-Marne", 
    "Cherbourg-en-Cotentin", "Mérignac", "Antibes", "Saint-Maur-des-Fossés", "Ajaccio", "Fort-de-France", 
    "Cannes", "Saint-Nazaire", "Noisy-le-Grand", "Mamoudzou", "Drancy", "Cergy", "Levallois-Perret", 
    "Issy-les-Moulineaux", "Calais", "Colmar", "Pessac", "Vénissieux", "Évry-Courcouronnes", "Clichy", 
    "Quimper", "Ivry-sur-Seine", "Valence", "Bourges", "Antony", "Cayenne", "La Seyne-sur-Mer", 
    "Montauban", "Troyes", "Villeneuve-d'Ascq", "Pantin", "Chambéry", "Niort", "Le Blanc-Mesnil", 
    "Neuilly-sur-Seine", "Sarcelles", "Fréjus", "Lorient", "Villejuif", "Saint-André", "Maisons-Alfort", 
    "Clamart", "Narbonne", "Meaux", "Beauvais", "Hyères", "Bobigny", "Vannes", "La Roche-sur-Yon", 
    "Saint-Louis", "Chelles", "Cholet", "Corbeil-Essonnes", "Épinay-sur-Seine", "Bayonne", "Saint-Ouen-sur-Seine", 
    "Saint-Quentin", "Cagnes-sur-Mer", "Fontenay-sous-Bois", "Vaulx-en-Velin", "Les Abymes", "Saint-Laurent-du-Maroni", 
    "Sevran", "Sartrouville", "Arles", "Bondy", "Gennevilliers", "Albi", "Massy", "Saint-Herblain", 
    "Laval", "Saint-Priest", "Suresnes", "Martigues", "Les Sables-d'Olonne", "Grasse", "Vincennes", 
    "Évreux", "Aubagne", "Bastia", "Saint-Malo", "Blois", "La Courneuve", "Brive-la-Gaillarde", "Meudon", 
    "Livry-Gargan", "Carcassonne", "Montrouge", "Choisy-le-Roi", "Rosny-sous-Bois", "Noisy-le-Sec", 
    "Talence", "Belfort", "Charleville-Mézières", "Alfortville", "Saint-Germain-en-Laye", "Sète", 
    "Alès", "Saint-Brieuc", "Chalon-sur-Saône", "Salon-de-Provence", "Tarbes", "Mantes-la-Jolie", "Puteaux", 
    "Istres", "Melun", "Bagneux", "Caluire-et-Cuire", "Rezé", "Châlons-en-Champagne", "Châteauroux", 
    "Valenciennes", "Bron", "Thionville", "Castres", "Arras", "Garges-lès-Gonesse", "Anglet", "Villenave-d'Ornon", 
    "Bourg-en-Bresse", "Bagnolet", "Angoulême", "Boulogne-sur-Mer", "Colomiers", "Wattrelos", "Compiègne", 
    "Poissy", "Gagny", "Draguignan", "Gap", "Stains", "Montélimar", "Le Cannet", "Marcq-en-Barœul", 
    "Douai", "Villepinte", "Le Lamentin"]  

# Lecture du fichier CSV avec les infos de trajets
df = pd.read_csv("C:/Users/dalia/Downloads/TABLEAU FINALE scraping.csv")

# Normalisation des textes pour matcher sans accent / majuscule
def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Commande slash Discord
@bot.tree.command(name="chat", description="Pose une question sur un trajet entre deux villes")
async def chat(interaction: discord.Interaction, question: str):
    question_clean = normalize_text(question)

    # Trouve les villes mentionnées dans la question même en partie
    villes_trouvees = []
    for ville in villes_connues:
        if normalize_text(ville) in question_clean:
            villes_trouvees.append(ville)

    if len(villes_trouvees) < 2:
        await interaction.response.send_message(
            "Je n'ai pas reconnu deux villes dans ta question. Essaie par exemple : 'Comment aller de Paris à Lyon ?'"
        )
        return

    ville1, ville2 = villes_trouvees[0], villes_trouvees[1]

    # Filtrage des trajets dans le DataFrame, peu importe l'ordre
    condition1 = (df["Départ"].str.lower() == ville1.lower()) & (df["Arrivée"].str.lower() == ville2.lower())
    condition2 = (df["Départ"].str.lower() == ville2.lower()) & (df["Arrivée"].str.lower() == ville1.lower())

    trajet = df[condition1 | condition2]

    if trajet.empty:
        await interaction.response.send_message(f"Je n'ai pas trouvé de trajet entre {ville1} et {ville2}. 😕")
        return

    # On prend la première ligne du résultat (tu peux améliorer pour montrer plusieurs trajets plus tard)
    row = trajet.iloc[0]

    reponse = (
        f"**Trajet {row['Départ']} → {row['Arrivée']}**\n"
        f"• 🕐 Départ : {row['Heure de départ']}\n"
        f"• 🕒 Durée : {row['Durée']}\n"
        f"• 🚉 Arrivée : {row['Heure d’arrivée']}\n"
        f"• 🚗 Transport : {row['Transport']}\n"
        f"• 💶 Prix : {row['Prix']}"
    )

    await interaction.response.send_message(reponse)




def normalize_text(text):
    # Mise en minuscules
    text = text.lower()
    # Supprime les accents
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    # Supprime les caractères spéciaux
    text = re.sub(r'[^\w\s]', '', text)
    # Supprime les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@bot.tree.command(name="chat", description="Pose une question sur les déplacements")
async def chat(interaction: discord.Interaction, question: str):
    original_question = question
    question = normalize_text(question)

    responses = {
        "comment aller de paris a lyon": "Tu peux prendre un train, un bus ou une voiture. Le train (TGV) est le plus rapide (~2h).",
        "prix moyen de marseille a toulouse": "Le prix en bus est autour de 15€, en train entre 30 et 60€, en fonction de la période.",
        "quel est le moyen le plus rapide pour aller de lille a nantes": "L’avion est le plus rapide (~1h20), mais le train reste pratique (~4h30).",
        "image paris lyon": "Voici un aperçu du trajet Paris → Lyon 🚄\nhttps://cdn.kimkim.com/files/a/maps/80fa0181a329d32c8a98cae9a2dfbf3b54134da4/big-a17d39e33d4127d054db903c45ca07a0.jpg",
        "combien de temps pour aller de bordeaux a nice": "En train : ~8h. En avion : ~1h30. En voiture : environ 9h selon le trafic.",
        "je veux aller de strasbourg a grenoble": "Tu peux prendre un train avec changement à Lyon. Durée estimée : 6h30.",
        "idee de road trip dans le sud de la france": "Pourquoi pas : Marseille → Toulon → Nice → Cannes 🚗☀️\nPense à visiter les calanques !",
        "comment aller a dijon depuis nancy": "Le train est direct et dure environ 2h. Il y a aussi des bus, moins chers mais plus longs (~3h).",
        "comment aller vite doreleans a rouen": "Voiture (~2h30) ou train (~3h avec un changement). Il n’y a pas de ligne directe rapide.",
        "quel est le trajet le moins cher de reims a metz": "Le bus est souvent le moins cher, parfois à partir de 5€. Compare sur Rome2rio !",
        "cest quoi le site rome2rio": "C’est une plateforme qui compare tous les moyens de transport pour un trajet : https://www.rome2rio.com/",
        "trajet paris lyon": "Train TGV : 2h / Bus : 6h / Voiture : 4h30. Prix variable selon le moment.",
        "idee de transport ecolo": "Favorise le train ou le covoiturage 🚆🌱",
        "le plus rapide toulouse bordeaux": "Train direct : 2h environ.",
        "meilleur prix nantes a lille": "Bus : dès 12€, mais durée > 8h. Train : 4h, dès 30€ avec anticipation."
    }

    # Normalisation des clés
    normalized_keys = list(responses.keys())

    # Trouver la question la plus proche
    closest_match = difflib.get_close_matches(question, normalized_keys, n=1, cutoff=0.6)

    if closest_match:
        response = responses[closest_match[0]]
    else:
        response = "Désolé, je ne connais pas encore cette question. Tu peux essayer avec une autre ! 😊"

    await interaction.response.send_message(response)


@bot.tree.command(name="warnguy", description="Alerter une personne")
async def warnguy(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message("Alerte envoyée")
    await member.send("Tu as reçu une alerte")

@bot.tree.command(name="banguy", description="Bannir une personne")
async def banguy(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message("Ban envoyé!")
    await member.ban(reason="Tu n'es pas abonné")
    await member.send("Tu as été banni")





# Démarrage du bot avec le token chargé depuis .env
bot.run(os.getenv('DISCORD_TOKEN'))
