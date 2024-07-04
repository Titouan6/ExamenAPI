from fastapi import FastAPI, HTTPException  # Importation des classes FastAPI et HTTPException depuis fastapi
from pydantic import BaseModel  # Importation de la classe BaseModel depuis pydantic pour la validation des données
import requests  # Importation de la bibliothèque requests pour effectuer des requêtes HTTP
from datetime import datetime, timedelta  # Importation des classes datetime et timedelta pour la gestion des dates et heures
from typing import Optional  # Importation du type Optional pour déclarer des paramètres facultatifs

app = FastAPI()  


API_KEY = "0c465c1ad28bc0e0f0e84b014687f6c9"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"  
CACHE = {}  # Dictionnaire vide pour stocker les données en cache
CACHE_EXPIRATION = timedelta(minutes=20)  # Durée d'expiration du cache (20 minutes)

# Modèle de données Pydantic pour représenter les données météorologiques
class WeatherData(BaseModel):
    temperature_actuelle: Optional[float]
    temperature_min: Optional[float]
    temperature_max: Optional[float]
    temperature_ressentie: Optional[float]
    humidite: Optional[int]
    pression: Optional[int]
    vent_vitesse: Optional[float]
    vent_direction: Optional[int]
    description: Optional[str]
    lever_soleil: Optional[str]
    coucher_soleil: Optional[str]
    visibilité: Optional[int]
    couverture_nuageuse: Optional[int]

# Fonction pour récupérer les données météorologiques depuis l'API OpenWeatherMap
def fetch_weather_data(city: str, country_code: str) -> dict:
    url = f"{BASE_URL}?q={city},{country_code}&appid={API_KEY}&units=metric"  # URL de requête avec la clé API et les paramètres
    response = requests.get(url)  # Envoi de la requête GET à l'API OpenWeatherMap
    if response.status_code == 200:  # Vérification si la requête a réussi (statut 200)
        return response.json()  # Conversion de la réponse JSON en dictionnaire Python
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from OpenWeatherMap")  # Gestion de l'erreur si la requête échoue

# Fonction pour transformer les données JSON en objet WeatherData
def parse_weather_data(data: dict) -> WeatherData:
    return WeatherData(
        temperature_actuelle=data["main"]["temp"],
        temperature_min=data["main"]["temp_min"],
        temperature_max=data["main"]["temp_max"],
        temperature_ressentie=data["main"]["feels_like"],
        humidite=data["main"]["humidity"],
        pression=data["main"]["pressure"],
        vent_vitesse=data["wind"]["speed"],
        vent_direction=data["wind"]["deg"],
        description=data["weather"][0]["description"],
        lever_soleil=datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S'),
        coucher_soleil=datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S'),
        visibilité=data.get("visibility", None),
        couverture_nuageuse=data["clouds"]["all"]
    )

# Route pour récupérer les données météorologiques d'une ville spécifique
@app.get("/weather/{city}/{country_code}", response_model=WeatherData)
def get_weather(city: str, country_code: str, fields: Optional[str] = None):
    cache_key = f"{city}_{country_code}"  # Clé unique pour chaque ville et code pays
    current_time = datetime.utcnow()  # Date et heure actuelle

    # Vérification si les données sont déjà en cache et n'ont pas expiré
    if cache_key in CACHE:
        cached_data, timestamp = CACHE[cache_key]  # Récupération des données et du timestamp du cache
        if current_time - timestamp < CACHE_EXPIRATION:  # Vérification de l'expiration du cache
            weather_data = cached_data  # Utilisation des données en cache
        else:
            weather_data = fetch_weather_data(city, country_code)  # Requête API si les données sont expirées
            CACHE[cache_key] = (weather_data, current_time)  # Mise à jour du cache avec les nouvelles données
    else:
        weather_data = fetch_weather_data(city, country_code)  # Requête API si les données ne sont pas en cache
        CACHE[cache_key] = (weather_data, current_time)  # Stockage des données dans le cache avec le timestamp actuel

    parsed_data = parse_weather_data(weather_data)  # Transformation des données JSON en objet WeatherData

    if fields:  # Vérification si des champs spécifiques sont demandés
        field_list = fields.split(",")  
        filtered_data = {field: getattr(parsed_data, field) for field in field_list if hasattr(parsed_data, field)}  # Filtrage des données demandées
        return filtered_data  # Renvoi des données filtrées si demandé

    return parsed_data  

# Route pour vider le cache
@app.get("/clear_cache")
def clear_cache():
    CACHE.clear()  
    return {"detail": "Cache cleared"}  

# Gestionnaire d'exceptions pour les erreurs HTTP
@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})  # Réponse JSON avec le détail de l'erreur HTTP
