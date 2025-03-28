import network, socket, uasyncio as asyncio
import json
from time import sleep
from machine import ADC, Pin
from picoder import LEDMATRIX, BUZZERTONE, BUTTON, LCD, BME280
import sys

# Initialisation des capteurs
bme280 = BME280()
sensor = ADC(27)
etat_direction=0

# Dictionnaire des correspondances entre les résistances et les directions du vent
resistance = {
    (49000, 51000): "Nord",
    (5000, 7000): "Est",
    (17000, 19000): "Sud",
    (59000, 61000): "Ouest",
}


# Informations WiFi
SSID = 'WIFI-SIN'
PASSWORD = '12345678'

# Configuration des serveurs
HTTP_PORT = 80
WS_PORT = 12345
HOST = "0.0.0.0"

# Connexion au WiFi
async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)
    wlan.connect(SSID, PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() in (network.STAT_GOT_IP, network.STAT_IDLE):
            break
        max_wait -= 1
        print('Connexion en cours...')
        await asyncio.sleep(1)

    if wlan.status() != network.STAT_GOT_IP:
        raise RuntimeError('Échec de connexion')
    else:
        print('Connexion réussie, IP:', wlan.ifconfig()[0])

# Récupération des données météo
def get_weather_data():
    return {
        "temperature": bme280.temperature(),
        "humidity": bme280.humidity(),
        "pressure": bme280.pressure(),
        "wind_direction": etat_direction
        }

# Gestion des requêtes HTTP
async def handle_http(reader, writer):
    request = await reader.read(1024)
response = """
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>    
<html lang="fr">
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Gidole&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined&display=swap">
    <link href="https://fonts.googleapis.com/css2?family=Urbanist:ital,wght@1,800&display=swap" rel="stylesheet">

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Station Météo</title>
    <link rel="icon" type="image/png" href="https://cdn-icons-png.flaticon.com/512/869/869869.png">
    <style>
        body {
            background: linear-gradient(to right, #2d8ee2, #044b4e);
            color: #fff;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .container {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            width: 90%;
            max-width: 400px;
            height: 380px;
            margin: 50px auto;
            padding: 25px;
            ;background: rgba(3, 238, 247, 0.2);
            border-radius: 15px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        }

        .title {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
        }
        
        h1 {
            font-size: 24px;
            font-family: "Urbanist", sans-serif;
            font-optical-sizing: auto;
            font-weight: 800;
            font-style: italic, underlines;
          }

        .info {
            font-size: 20px;
            margin: 10px 0;
        }
        .icon {
            font-size: 50px;
            margin: 10px 0;
        }

        .button {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
        }

        .refresh-btn {
            justify-content: center;
            display: flex;
            align-items: center;
            gap: 5px;
            margin-top: auto;
            margin-left: 19%;
            margin-right: 18%;
            padding: 10px 15px;
            font-size: 16px;
            color: #fff;
            background: #e16827;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .refresh-btn:hover {
            background: #ea8e04;
        }

        .pressure, .humidity, .temperature, .girouette, .anémo{
            font-size: 19px;
            font-family: "Gidole", sans-serif;
            font-weight: 400;
            font-optical-sizing: auto;
            font-style: italic;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
        }

        .material-symbols-outlined {
            font-variation-settings:
            'FILL' 1,
            'wght' 350,
            'GRAD' 0,
            'opsz' 24;
            color: rgb(255, 204, 0);
        }

    </style>
</head>
<body>

    <div class="container">

        <div>
            <div class="title">
                <span class="material-symbols-outlined">clear_day</span>
                <h1>Station Météo</h1>
            </div>

            <div class="temperature">
                <span class="material-symbols-outlined">thermometer</span>
                <div class="info">Température: <span id="temperature">--</span></div>  <!--remplacer span par : <span id="temperature">""" + str(temperature) + """ </span>-->  
            </div>

            <div class="humidity">
                <span class="material-symbols-outlined">water_drop</span>
                <div class="info"> Humidité: <span id="humidity">--</span>%</div>
            </div>

            <div class="pressure">
                <span class="material-symbols-outlined">air</span>
                <div class="info">Pression: <span id="pressure">--</span>hPa</div>
            </div>

            <div class="anémo">
                <span class="material-symbols-outlined">wind_power</span>
                <div class="info">Vitesse du vent: <span id="air_speed">--</span>km/h</div>
            </div>
         
            <div class="girouette">
                <span class="material-symbols-outlined">air</span>
                <div class="info">Direction du vent: <span id="wind_direction">--</span></div>
            </div>
            

        </div>
        
        <button class="refresh-btn" onclick="document.location.reload()">
            <span class="material-symbols-outlined">autorenew</span> Mettre à jour
        </button>

    </div>

</body>
"""

    await writer.awrite(response.encode())
    await writer.aclose()

# Gestion du serveur WebSocket
async def websocket_server(reader, writer):
    try:
        while True:
            global valeur
            valeur = sensor.read_u16()  # Lire la valeur ADC sur 16 bits (PiCoder)
            weather_data = json.dumps(get_weather_data())
            await writer.awrite(weather_data.encode('utf-8'))
            await asyncio.sleep(2)
    except Exception as e:
        print(f"Client déconnecté: {e}")
    finally:
        await writer.aclose()

# Lancement des serveurs
async def start_servers():
    await asyncio.start_server(handle_http, HOST, HTTP_PORT)
    await asyncio.start_server(websocket_server, HOST, WS_PORT)
    print(f"Serveurs démarrés sur HTTP:{HTTP_PORT} et WebSocket:{WS_PORT}")

# Fonction principale
async def main():
    await connect_wifi()
    await start_servers()
    while True:
        await asyncio.sleep(10)

asyncio.run(main())
