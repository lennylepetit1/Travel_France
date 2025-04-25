import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import difflib
import unicodedata
import re



# Charger les variables d'environnement depuis le fichier .env
load_dotenv()  

print("Lancement du bot...")




# Création de l'instance du client avec les intents appropriés
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot allumé !")
    # Synchroniser les commandes slash
    try:
        # Synchronisation des commandes
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Une erreur est survenue lors de la synchronisation des commandes : {e}")

# Fonction de normalisation de texte (suppression des accents, minuscules, etc.)
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

# Commande slash pour poser une question sur les déplacements
@bot.tree.command(name="chat", description="Pose une question sur les déplacements")
async def chat(interaction: discord.Interaction, question: str):
    original_question = question
    question = normalize_text(question)

    # Dictionnaire des réponses possibles
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
        "meilleur prix nantes a lille": "Bus : dès 12€, mais durée > 8h. Train : 4h, dès 30€ avec anticipation.",
      "comment aller de paris a marseille": "Train TGV direct (~3h), bus (~10h) ou avion (~1h30).",
    "quel est le moyen le plus rapide pour aller de lyon a toulouse": "L’avion (~1h10) est le plus rapide, mais le train direct (~4h30) est confortable.",
    "combien coute un trajet lille strasbourg": "En train, entre 40€ et 90€. En bus, à partir de 20€.",
    "moyen le moins cher pour aller de nantes a bordeaux": "Le bus est souvent le moins cher, à partir de 10€.",
    "idee de trajet pour visiter la bretagne": "Départ de Rennes → Saint-Malo → Brest → Quimper 🚗🌊",
    "temps de trajet entre dijon et lyon": "En train : environ 2h. En voiture : 2h15.",
    "comment aller de grenoble a montpellier": "Train avec changement à Valence ou Lyon (~3h30).",
    "quel transport entre metz et paris": "Train direct (TGV) ~1h30. Bus plus lent (~4h).",
    "moyen le plus ecolo pour aller de tours a poitiers": "Le train régional est rapide (~1h) et écologique.",
    "trajet rapide de nice a avignon": "Train avec changement à Marseille (~3h30).",
    "itineraire de road trip entre lyon et nimes": "Lyon → Valence → Avignon → Nîmes 🚘☀️",
    "comment aller de caen a rouen": "Train direct (~1h30) ou voiture (~1h45).",
    "quel est le prix moyen pour aller de paris a lille": "Train TGV : entre 25€ et 60€. Bus : dès 10€.",
    "temps de trajet en train de toulouse a montpellier": "Environ 2h15 en train direct.",
    "comment aller de bordeaux a bayonne": "Train direct (~2h10) ou voiture (~2h15).",
    "idee de voyage entre strasbourg et colmar": "Train régional rapide (~30 min), parfait pour une escapade.",
    "quel est le moyen le plus rapide de marseille a nice": "Train direct (~2h30), ou voiture (~2h20 sans bouchons).",
    "prix d un billet bus lyon grenoble": "Entre 5€ et 10€ selon la période.",
    "comment aller a annecy depuis geneve": "Bus ou train (~1h30), ou voiture (~45 min).",
    "trajet rapide entre paris et chartres": "Train TER direct (~1h) ou voiture (~1h15).",
    "idee de road trip entre clermont ferrand et limoges": "Clermont → Montluçon → Guéret → Limoges 🚙🌳",
    "temps en train de reims a paris": "Environ 45 minutes avec le TGV.",
    "comment aller de bordeaux a toulon": "Avion avec escale ou train avec changement (~7h).",
    "prix d un billet de nancy a strasbourg": "Entre 15€ et 30€ selon le mode et l’horaire.",
    "moyen le plus pratique de nantes a angers": "Train direct (~40 min) très fréquent.",
    "quelle duree pour aller de lille a bruxelles": "Environ 35 minutes en train Thalys ou TGV.",
    "comment aller a limoges depuis paris": "Train direct (~3h15) ou bus (~5h).",
    "quel transport de besancon a dijon": "Train TER (~1h30) ou voiture (~1h20).",
    "idee d itineraire de toulouse a carcassonne": "Toulouse → Castelnaudary → Carcassonne en train (~1h10).",
    "comment aller de perpignan a montpellier": "Train direct (~1h40), ou bus (~2h30).",
    "comment aller de pau a toulouse": "Train (~2h30) ou voiture (~2h15). Le bus est aussi une option moins chère.",
    "itineraire rapide entre tours et paris": "TGV direct : ~1h10. Voiture : ~2h30 selon le trafic.",
    "meilleur moyen de transport entre le mans et rennes": "Train direct (~1h30) ou voiture (~2h).",
    "comment aller de la rochelle a nantes": "Train avec ou sans changement (~2h30).",
    "quelle est la distance entre grenoble et chambery": "Environ 60 km, 1h en train ou voiture.",
    "trajet entre dijon et besancon": "Train TER direct (~1h30) ou voiture (~1h20).",
    "moyen de transport entre limoges et poitiers": "Train régional (~2h), peu de bus directs.",
    "temps de trajet de strasbourg a luxembourg": "Train direct (~2h10) ou voiture (~2h).",
    "comment aller de paris a bruxelles": "TGV Thalys : ~1h20. Bus : ~4h. Avion déconseillé.",
    "idee de road trip en normandie": "Rouen → Étretat → Deauville → Caen 🚗🌊",
    "combien coute un trajet paris chartres": "Entre 12€ et 20€ en train selon l’heure.",
    "meilleure option entre montpellier et perpignan": "Train direct (~1h40). Bus moins cher (~2h30).",
    "comment aller de lyon a annecy": "Train direct (~2h) ou voiture (~1h40).",
    "itineraire pour aller de metz a nancy": "Train (~50 min) ou voiture (~1h). Très facile.",
    "comment aller de bayonne a biarritz": "Train ou bus local (~15 min), ou vélo en bord de mer.",
    "trajet rapide entre angers et le mans": "Train direct (~40 min), très pratique.",
    "comment aller de paris a rouen": "Train direct (~1h30) ou voiture (~2h).",
    "temps de trajet de clermont ferrand a saint etienne": "Environ 2h en voiture. Train avec changement (~2h30).",
    "quelle option pour aller de toulon a marseille": "Train TER rapide (~1h15), ou voiture (~1h10).",
    "trajet entre avignon et arles": "Train direct (~20 min) ou voiture (~40 min).",
    "idee de boucle en road trip autour de bordeaux": "Bordeaux → Arcachon → Dune du Pilat → Saint-Émilion 🚘🍷",
    "temps de trajet entre lille et valenciennes": "Train TER (~40 min) ou voiture (~1h).",
    "comment aller de nancy a luxembourg": "Train direct (~1h30) ou voiture (~1h45).",
    "quelle est la meilleure façon d aller de lyon a geneve": "Train direct (~2h) ou covoiturage (~1h45).",
    "transport entre bordeaux et toulouse": "Train direct (~2h). Bus plus long mais moins cher.",
    "comment aller de caen a le havre": "Train avec changement (~2h30) ou voiture (~1h45).",
    "meilleur moyen de transport entre montpellier et nimes": "Train TER direct (~30 min), rapide et fréquent.",
    "idee de road trip entre toulouse et biarritz": "Toulouse → Auch → Pau → Biarritz 🚗🌄🌊",
    "quelle duree entre perpignan et narbonne": "Train direct (~40 min) ou voiture (~1h).",
    "comment aller de strasbourg a bale": "Train direct (~1h30) ou voiture (~1h45).",
   "quelle est la duree entre paris et amiens": "Train direct : ~1h15. Voiture : ~1h45 selon trafic.",
    "comment aller de grenoble a valence": "Train direct (~1h15) ou voiture (~1h).",
    "trajet entre nimes et avignon": "Train direct : ~30 minutes. Très pratique.",
    "idee de trajet entre dijon et lyon": "TGV direct (~2h). Voiture : ~2h également.",
    "meilleur itineraire entre orleans et chartres": "Train (~1h10) ou voiture (~1h20).",
    "comment aller de toulon a nice": "Train direct (~2h), ou voiture (~2h10).",
    "temps de trajet entre caen et cherbourg": "Train direct (~2h10).",
    "comment aller de bayonne a pau": "Train (~1h), ou voiture (~1h20).",
    "quelle est la distance entre le havre et rouen": "Environ 90 km, 1h15 en voiture ou train.",
    "comment aller de besancon a mulhouse": "Train direct (~1h30) ou voiture (~1h50).",
    "idee de week end depuis strasbourg": "Strasbourg → Colmar → Riquewihr 🚗🍇",
    "meilleur moyen entre tours et poitiers": "Train direct (~1h10) ou voiture (~1h30).",
    "comment aller de limoges a clermont ferrand": "Train (~3h) ou voiture (~2h45).",
    "itineraire de metz a reims": "Train direct (~2h) ou voiture (~2h15).",
    "trajet rapide entre rennes et brest": "Train direct (~2h15).",
    "comment aller de paris a lille": "TGV direct (~1h), ou bus (~3h).",
    "moyen de transport entre dijon et paris": "TGV direct (~1h40).",
    "quelle duree entre lyon et toulouse": "Avion (~1h10), train (~4h), voiture (~6h).",
    "comment aller de grenoble a chamonix": "Train + bus (~3h) ou voiture (~2h30).",
    "idee de circuit entre montpellier et carcassonne": "Montpellier → Béziers → Narbonne → Carcassonne 🚗🏰",
    "comment aller de rouen a amiens": "Train (~2h avec changement), ou voiture (~2h).",
    "trajet entre bordeaux et bayonne": "Train direct (~2h).",
    "quelle est la duree entre toulouse et albi": "Train (~1h) ou voiture (~1h10).",
    "comment aller de reims a lille": "Train direct (~2h15).",
    "transport entre besancon et dijon": "Train direct (~1h30).",
    "idee de road trip dans le massif central": "Clermont-Ferrand → Le Puy-en-Velay → Mende → Millau 🚗🌄",
    "quelle option pour aller de paris a le mans": "TGV direct (~1h).",
    "comment aller de nice a menton": "Train TER (~40 min) ou voiture (~50 min).",
    "duree de trajet entre nancy et strasbourg": "Train (~1h30), très simple.",
    "comment aller de limoges a brive la gaillarde": "Train direct (~1h30) ou voiture (~1h20).",
    "comment aller de lyon a annecy": "Train direct (~1h20) ou voiture (~1h30).",
    "trajet rapide entre dijon et nancy": "Train direct (~2h), ou voiture (~2h30).",
    "quelle est la duree entre paris et la rochelle": "TGV direct (~2h30), ou voiture (~5h).",
    "comment aller de rouen a calais": "Train avec changement (~2h30), ou voiture (~2h).",
    "comment aller de bordeaux a angouleme": "Train direct (~1h), ou voiture (~1h30).",
    "moyen de transport entre toulouse et montauban": "Train direct (~30 min), ou voiture (~40 min).",
    "trajet entre nantes et la roche sur yon": "Train direct (~1h), ou voiture (~1h15).",
    "comment aller de lyon a marseille": "TGV direct (~1h40), ou voiture (~3h).",
    "quel est le trajet le plus rapide entre rouen et le havre": "Train direct (~45 min), ou voiture (~1h).",
    "quelle est la distance entre toulouse et castres": "Train (~1h10), ou voiture (~1h30).",
    "comment aller de brest a quimper": "Train (~1h), ou voiture (~1h15).",
    "trajet entre strasbourg et mulhouse": "Train direct (~1h10), ou voiture (~1h).",
    "moyen de transport entre marseille et aix en provence": "Train direct (~30 min), ou voiture (~30 min).",
    "quelle est la duree entre paris et orleans": "Train (~1h), ou voiture (~1h30).",
    "comment aller de nantes a lorient": "Train direct (~1h30), ou voiture (~1h45).",
    "comment aller de nice a monaco": "Train direct (~25 min), ou voiture (~30 min).",
    "trajet entre lyon et montpellier": "TGV (~1h40), ou voiture (~3h).",
    "duree de trajet entre lille et rouen": "Train (~3h) ou voiture (~2h30).",
    "comment aller de metz a strasbourg": "Train direct (~2h), ou voiture (~2h).",
    "moyen de transport entre paris et troyes": "Train direct (~1h30), ou voiture (~1h45).",
    "quel est le moyen le plus rapide entre nantes et rennes": "Train (~40 min), ou voiture (~1h10).",
    "quelle est la distance entre clermont ferrand et montpellier": "Train (~3h), ou voiture (~3h30).",
    "comment aller de rouen a dieppe": "Train direct (~1h30), ou voiture (~1h).",
    "trajet entre toulouse et carcassonne": "Train direct (~1h), ou voiture (~1h10).",
    "quelle est la duree de trajet entre paris et reims": "Train direct (~45 min), ou voiture (~1h30).",
    "comment aller de lyon a valence": "Train direct (~1h), ou voiture (~1h30).",
    "moyen de transport entre marseille et montpellier": "Train direct (~1h30), ou voiture (~2h).",
    "comment aller de la rochelle a bordeaux": "Train direct (~2h), ou voiture (~2h).",
    "quelle est la distance entre dijon et lyon": "Train direct (~2h), ou voiture (~1h30).",
    "trajet rapide entre paris et montargis": "Train (~1h), ou voiture (~1h30).",
    "comment aller de lille a roubaix": "Train direct (~15 min), ou voiture (~20 min).",
    "quelle est la duree entre strasbourg et colmar": "Train direct (~30 min), ou voiture (~40 min).",
    "comment aller de toulon a marseille": "Train direct (~1h), ou voiture (~1h20)." }

    # Normalisation des clés du dictionnaire
    normalized_keys = list(responses.keys())

    # Trouver la question la plus proche
    closest_match = difflib.get_close_matches(question, normalized_keys, n=1, cutoff=0.6)

    if closest_match:
        response = responses[closest_match[0]]
    else:
        response = "Désolé, je ne connais pas encore cette question. Tu peux essayer avec une autre ! 😊"

    await interaction.response.send_message(response)

# Commande pour envoyer une alerte à un membre
@bot.tree.command(name="warnguy", description="Alerter une personne")
async def warnguy(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message("Alerte envoyée")
    await member.send("Tu as reçu une alerte")

# Commande pour bannir un membre
@bot.tree.command(name="banguy", description="Bannir une personne")
async def banguy(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message("Ban envoyé!")
    await member.ban(reason="Tu n'es pas abonné")
    await member.send("Tu as été banni")

# Démarrer le bot avec le token chargé depuis les variables d'environnement
print(f"TOKEN lu depuis .env : {os.getenv('TOKEN')}")

bot.run(os.getenv("TOKEN"))




