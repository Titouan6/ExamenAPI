#Requêtes vers l'API Open Weather app
Il faut installer dans le terminal : pip install requests
ensuite une fois qu'on a le code, toujours dans le terminal pour executer le script : python meteo.py
Et on va avoir les données avec les requêtes qu'on a demandé


#Devéloppement de l'API avec Fast APi
On va installer dans le terminal: FastAPI,uvicorn pour le serveur et ainsi que de la bibliothèque requests pour les requêtes à l'API OpenWeatherMap : pip install fastapi uvicorn requests
Ensuite on va faire le code pour créer l'application FastAPI
et apres pour lancer l'appli il faut mettre dans le terminal : uvicorn main:app --reload
sur la navigateur, on va sur : http://127.0.0.1:8000/docs#/ pour tester si ca marche
On arrive donc sur l'Appli FastApi et on peut tester les diférentes routes et voir si notre code marche
De mon coté pour filter les données ca marche pas mais le reste c'est bon
