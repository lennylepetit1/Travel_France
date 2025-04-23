import requests
import pandas as pd
from datetime import datetime, timedelta
import random
import time
import itertools

# Fonction pour convertir des minutes en "x h y min"
def minutes_to_heure_minutes(m):
    try:
        h = int(m) // 60
        m = int(m) % 60
        return f"{h} h {m} min"
    except:
        return "Durée invalide"

# Liste des 200 villes françaises distinctes
villes = [
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Montpellier", "Strasbourg", 
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
    "Douai", "Villepinte", "Le Lamentin"
]

# Génération des paires de villes
paires = list(itertools.permutations(villes, 2))
tous_les_resultats = []

# Pour chaque combinaison de départ et d'arrivée
for depart, arrivee in paires:
    print(f"Trajet : {depart} → {arrivee}")

    # Paramètres pour la requête API
    url = "https://www.rome2rio.com/api/1.5/json/search"
    params = {
        "key": "jGq3Luw3", 
        "oName": depart,
        "dName": arrivee,
        "languageCode": "fr", 
        "currencyCode": "EUR",
        "uid": "TWTai20250331133056035ufgd",
        "aqid": "FRStr20250407071731790ufgd",
        "analytics": "true",
        "groupOperators": "true",
        "noAir": "false",
        "noPrice": "false"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        routes = data.get("routes", [])

        # Pour chaque mode de transport, trouver le trajet le moins cher
        for mode in ['Train', 'Bus', 'Avion', 'Covoiturage']:
            min_price = float("inf")  # Initialisation avec une valeur infinie
            best_route = None

            for route in routes:
                if mode in route.get("name", ""):  # Vérification du mode de transport
                    # Durée du trajet (en secondes)
                    duree_sec = route.get("duration", None)
                    duree_min = duree_sec / 60 if duree_sec else None
                    duree_formatee = minutes_to_heure_minutes(duree_min) if duree_min else "Non précisé"

                    # Générer la date et l'heure de départ aléatoires dans la plage du 28 avril au 1er mai
                    jours_alea = random.randint(0, 3)
                    heure_alea = random.randint(6, 20)
                    minute_alea = random.choice([0, 15, 30, 45])
                    date_depart = datetime(2025, 4, 28).replace(hour=heure_alea, minute=minute_alea, second=0, microsecond=0) + timedelta(days=jours_alea)
                    date_depart_str = date_depart.strftime("%d/%m/%Y")
                    heure_depart_str = date_depart.strftime("%H:%M")
                    heure_arrivee_str = (date_depart + timedelta(minutes=duree_min)).strftime("%H:%M") if duree_min else "Non précisé"

                    # Prix du trajet (prix le plus bas possible)
                    p = route.get("indicativePrices", [])
                    if p and isinstance(p, list):
                        p0 = p[0]
                        if "priceLow" in p0:
                            prix = int(p0['priceLow'])
                        elif "price" in p0:
                            prix = int(p0['price'])
                        else:
                            prix = float("inf")
                    else:
                        prix = float("inf")

                    # Vérification du prix le plus bas pour ce mode de transport
                    if prix < min_price:
                        min_price = prix
                        best_route = route

            # Si un trajet avec prix a été trouvé pour ce mode de transport, on l'ajoute
            if best_route:
                mode = best_route.get("name", "").replace(",", " ")
                # Formatage des données avec le trajet le moins cher
                tous_les_resultats.append({
                    "Départ": depart,
                    "Arrivée": arrivee,
                    "Date de départ": date_depart_str,
                    "Heure de départ": heure_depart_str,
                    "Durée": duree_formatee,
                    "Heure d’arrivée": heure_arrivee_str,
                    "Transport": mode,
                    "Prix": f"{min_price} €"
                })

        # Attendre avant la prochaine requête pour éviter la surcharge des serveurs
        time.sleep(1)

    except Exception as e:
        print(f"Erreur pour {depart} → {arrivee} :", e)
        continue

# Création du DataFrame et sauvegarde dans un fichier CSV
df = pd.DataFrame(tous_les_resultats)
df.to_csv("resultats_toutes_villes.csv", index=False, sep=";", encoding="utf-8-sig")
print("\n✅ Fichier généré : resultats_toutes_villes.csv")
