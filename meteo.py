import requests
from datetime import datetime

ville = "Francheville"
code_pays = "fr"
cle_api = "0c465c1ad28bc0e0f0e84b014687f6c9" 

url = f"http://api.openweathermap.org/data/2.5/weather?q={ville},{code_pays}&appid={cle_api}&units=metric"

response = requests.get(url)
data = response.json()

if data["cod"] == 200:
    temperature_actuelle = data["main"]["temp"]
    temperature_min = data["main"]["temp_min"]
    temperature_max = data["main"]["temp_max"]
    temperature_ressentie = data["main"]["feels_like"]
    
    humidite = data["main"]["humidity"]
    
    pression = data["main"]["pressure"]
    
    vent_vitesse = data["wind"]["speed"]
    vent_direction = data["wind"]["deg"]
    
    description = data["weather"][0]["description"]
    
    lever_soleil = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
    coucher_soleil = datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')
    
    visibilité = data.get("visibility", "N/A")
    
    couverture_nuageuse = data["clouds"]["all"]
    
    print(f"Température actuelle à {ville}: {temperature_actuelle} °C")
    print(f"Température minimale: {temperature_min} °C")
    print(f"Température maximale: {temperature_max} °C")
    print(f"Température ressentie: {temperature_ressentie} °C")
    print(f"Humidité: {humidite}%")
    print(f"Pression atmosphérique: {pression} hPa")
    print(f"Vitesse du vent: {vent_vitesse} m/s")
    print(f"Direction du vent: {vent_direction}°")
    print(f"Description: {description}")
    print(f"Heure du lever du soleil: {lever_soleil}")
    print(f"Heure du coucher du soleil: {coucher_soleil}")
    print(f"Visibilité: {visibilité} mètres")
    print(f"Couverture nuageuse: {couverture_nuageuse}%")
else:
    print("Erreur lors de la récupération des données météorologiques.")

