import network, socket, uasyncio as asyncio
from time import sleep
import urequests as requests
from machine import ADC, Pin
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
sensor = ADC(27)  # Utilisation directe du canal ADC sur PiCoder

# Informations WiFi
ssid = 'WIFI-SIN'
password = '12345678'

HOST = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
PORT = 80       # Port d'écoute

temperature = 0
humidity = 0
pressure = 0

async def get_wind_direction(valeur):
        global etat_direction
        for (minimum, maximum), direction in resistance.items():
            if minimum <= value <= maximum:
                etat_direction=direction
                return direction
        
        return etat_direction


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
                <div class="info">Température: <span id="temperature"> """+ str(temperature)+"""</span></div> 
            </div>

            <div class="humidity">
                <span class="material-symbols-outlined">water_drop</span>
                <div class="info"> Humidité: <span id="humidity">"""+ str(humidity)+"""</span></div>
            </div>

            <div class="pressure">
                <span class="material-symbols-outlined">air</span>
                <div class="info">Pression: <span id="pressure">"""+ str(pressure) +"""</span>hPa</div>
            </div>

            <div class="anémo">
                <span class="material-symbols-outlined">wind_power</span>
                <div class="info">Vitesse du vent: <span id="air_speed">--</span>km/h</div>
            </div>
         
            <div class="girouette">
                <span class="material-symbols-outlined">air</span>
                <div class="info">Direction du vent: <span id="wind_direction"> """ +str(etat_direction)+"""</span></div>
            </div>
            

        </div>
        
        <button class="refresh-btn" onclick="document.location.reload()">
            <span class="material-symbols-outlined">autorenew</span> Mettre à jour
        </button>

    </div>

</body>

<script>
    const ws = new WebSocket("ws://" + window.location.host + ":80");

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        document.getElementById("temperature").innerText = data.temperature;
        document.getElementById("humidity").innerText = data.humidity;
        document.getElementById("pressure").innerText = data.pressure;
    };

    ws.onerror = function(error) {
        console.error("Erreur WebSocket :", error);
    };
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


async def check_humidity():
    global humidity
    humidity = bme280.humidity()	# provides relative Humidity in percentage
        
async def check_pressure():
    global pressure
    pressure = bme280.pressure() # provides relative pressure in hPa
    
async def check_temperature():
    global temperature
    temperature = bme280.temperature()
    
async def check_wind_direction():
    global wind_direction, etat_direction,resistance
    
    etat_direction=0
    # Dictionnaire des correspondances entre les résistances et les directions du vent
    resistance = {
        (49000, 51000): "Nord",
        (5000, 7000): "Est",
        (17000, 19000): "Sud",
        (59000, 61000): "Ouest",
    }
    
    wind_direction = etat_direction
        
            

    await asyncio.sleep(0.01)

# Fonction principale
async def main():
    
    await connect_wifi()
    asyncio.create_task(check_humidity())
    asyncio.create_task(check_pressure())
    asyncio.create_task(check_temperature())
    asyncio.create_task(check_wind_direction())
    asyncio.create_task(shutdown_button())
    asyncio.create_task(start_server())
    
    
    
    while True:
        global valeur
        valeur = sensor.read_u16()
        await asyncio.sleep(1)

asyncio.run(main())