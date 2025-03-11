import network, socket, uasyncio as asyncio
from time import sleep
import urequests as requests
from picoder import LED, BUTTON, LCD, LEDMATRIX, BUZZERTONE, RGB, BME280
import sys

# Initialisation des composants matériels
ledmatrix = LEDMATRIX()
bzrtone = BUZZERTONE()
btn1 = BUTTON(1)
btn2 = BUTTON(2)
btn3 = BUTTON(3)
btn4 = BUTTON(4)
display = LCD()
bme280 = BME280()

# Informations WiFi
ssid = 'WIFI-SIN'
password = '12345678'

HOST = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
PORT = 80       # Port d'écoute

temperature = 0
humidity = 0
pressure = 0

# Connexion au WiFi
async def connect_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() in (network.STAT_GOT_IP, network.STAT_IDLE):
            break
        max_wait -= 1
        print('Connexion en cours...')
        await asyncio.sleep(1)

    if wlan.status() != network.STAT_GOT_IP:
        raise RuntimeError('Echec de connexion')
    else:
        print('\nConnexion reussie')
        print('IP:', wlan.ifconfig()[0])


# Gestion des requêtes HTTP entrantes
async def handle_client(reader, writer):
    await check_humidity()
    await check_pressure()
    
    request = await reader.read(1024)
    response = """
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Station Météo</title>
    <link rel="icon" type="image/png" href="https://cdn-icons-png.flaticon.com/512/869/869869.png">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: #fff;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 90%;
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }
        .info {
            font-size: 20px;
            margin: 10px 0;
        }
        .icon {
            font-size: 50px;
            margin: 10px 0;
        }
        .refresh-btn {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 15px;
            font-size: 16px;
            color: #fff;
            background: #ff9800;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .refresh-btn:hover {
            background: #e68900;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>🌤️ Station Météo</h1>
        <div class="info">🌡️ Température: <span id="temperature">""" + str(temperature) + """°C </span></div>
        <div class="info">💧 Humidité: <span id="humidity"> """ + str(humidity) + """</span></div>
        <div class="info">🌬️ Pression: <span id="pressure"> """ + str(pressure) + """hPa </span></div>
        <button class="refresh-btn" onclick="document.location.reload()">🔄 Mettre à jour</button>
    </div>

</body>
<script>
setTimeout(() =>{document.location.reload()}, 1500)
</script>
</html>

"""
    await writer.awrite(response.encode())
    await writer.aclose()

# Démarrage du serveur HTTP
async def start_server():
    
    await asyncio.start_server(handle_client, HOST , PORT)
    print("\nServeur connecte sur", wlan.ifconfig()[0], "et sur le port",PORT)

# Surveillance du bouton pour arrêter le serveur
async def shutdown_button():
    
    while True:
        
        if btn4.read() == 1:
            print("\nArret du serveur.")
            sys.exit()
            break
        
        await asyncio.sleep(0.1)

# Affichage du menu sur l'écran LCD
async def display_menu():
    
    display.draw_text8x8(1, 210, "BTN1 = EPHEMERIDE", RGB(255, 0, 0))
    display.draw_text8x8(1, 225, "BTN2 = METEO", RGB(0, 255, 0))
    display.draw_text8x8(117, 225, "BTN3 = TIME", RGB(0, 0, 255))

# Récupération des données météo
async def fetch_weather():
    res_weather= requests.get(url='https://api.open-meteo.com/v1/forecast?latitude=46.19737&longitude=5.22305&current=temperature_2m,precipitation,wind_speed_10m&timezone=auto&forecast_days=1')
    return res_weather.json()["current"]

# Récupération des données de sunrise
async def fetch_sunrise():
    res_sunrise =requests.get(url='https://api.sunrisesunset.io/json?lat=46.20574&lng=5.2258')
    return res_sunrise.json()["results"]

# Récupération des données de time
async def fetch_time():
    res_time =requests.get(url='https://timeapi.io/api/time/current/zone?timeZone=Europe%2FParis')
    return res_time.json()

async def check_humidity():
    global humidity
    humidity = bme280.humidity()	# provides relative Humidity in percentage
        
async def check_pressure():
    global pressure
    pressure = bme280.pressure()	# provides relative pressure in hPa
        

# Gestion dees boutons pour afficher les informations
async def button_listener():
    global temperature

    
    while True:
        
        if btn1.read() == 1:
            bzrtone.play(750,5000)
            await asyncio.sleep(1)
            bzrtone.stop()
            sunrise = await fetch_sunrise()
            bzrtone.play(1500,5000)
            await asyncio.sleep(1)
            bzrtone.stop()
            display.clear()
            display.draw_text8x8(0, 20, f"Lever du soleil: {sunrise['sunrise']}",RGB(255, 255, 255))
            display.draw_text8x8(0, 35, f"Coucher du soleil: {sunrise['sunset']}", RGB(255, 255, 255))
            await display_menu()
            
        elif btn2.read() == 1:
            bzrtone.play(750,5000)
            await asyncio.sleep(1)
            bzrtone.stop()
            weather = await fetch_weather()
            temperature = weather["temperature_2m"]
            bzrtone.play(1500,5000)
            await asyncio.sleep(1)
            bzrtone.stop()
            display.clear()
            display.draw_text8x8(0, 20, f"Il fait {temperature} degres",RGB(255, 255, 255))
            display.draw_text8x8(0, 35, f"Il pleut actuellement a {weather["precipitation"]} mm.",RGB(255, 255, 255))
            display.draw_text8x8(0, 50, f"Ca souffle dehors a {weather["wind_speed_10m"]} km/h.",RGB(255, 255, 255))
            await display_menu()
            
            
        elif btn3.read() == 1:
            bzrtone.play(750,5000)
            await asyncio.sleep(1)
            bzrtone.stop()
            time = await fetch_time()
            bzrtone.play(1500,5000)
            await asyncio.sleep(1)
            bzrtone.stop()
            display.clear()
            display.draw_text8x8(0, 20, f"Date: {time['date']}", RGB(255, 255, 255))
            display.draw_text8x8(0, 35, f"Heure: {time['time']}", RGB(255, 255, 255))
            await display_menu()
            
        await asyncio.sleep(0.01)

# Fonction principale
async def main():
    
    await connect_wifi()
    asyncio.create_task(start_server())
    asyncio.create_task(display_menu())
    asyncio.create_task(button_listener())
    asyncio.create_task(shutdown_button())
    
    
    
    while True:
        await asyncio.sleep(1)

asyncio.run(main())