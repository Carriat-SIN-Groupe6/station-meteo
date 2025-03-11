import network, socket, uasyncio as asyncio
from picoder import LED, BUTTON, LCD
import sys

# Initialisation des composants
led = LED(1), LED(2)
btn4 = BUTTON(4)
display = LCD()

# Paramètres du réseau
ssid = 'WIFI-SIN'
password = '12345678'

async def connect_wifi():
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

async def handle_client(reader, writer):
    """Gère les requêtes HTTP entrantes."""
    request = await reader.read(1024)
    print("\nRequete recue:", request.decode())

    response = """\
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
        <div class="info">🌡️ Température: <span id="temperature">--</span>°C</div>
        <div class="info">💧 Humidité: <span id="humidity">--</span>%</div>
        <div class="info">🌬️ Pression: <span id="pressure">--</span> hPa</div>
        <button class="refresh-btn" onclick="updateWeather()">🔄 Mettre à jour</button>
    </div>

    <script>
        function updateWeather() {
            fetch('/data')  // Appelle une API locale ou distante (à adapter selon ton serveur)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("temperature").innerText = data.temperature;
                    document.getElementById("humidity").innerText = data.humidity;
                    document.getElementById("pressure").innerText = data.pressure;
                })
                .catch(error => console.error("Erreur lors de la récupération des données météo :", error));
        }

        // Met à jour les données au chargement de la page
        updateWeather();
    </script>

</body>
</html>


"""
    await writer.awrite(response.encode())
    await writer.aclose()

async def start_server():
    """Lance un serveur HTTP asynchrone en MicroPython."""
    print("\nServeur en attente de connexion...")
    await asyncio.start_server(handle_client, "0.0.0.0", 80)

async def monitor_button():
    """Surveille le bouton et arrête le serveur si pressé."""
    while True:
        if btn4.read() == 1:
            print("\nArret du serveur.")
            sys.exit()
            break
        await asyncio.sleep(0.1)

async def main():
    await connect_wifi()
    asyncio.create_task(start_server())  # Lance le serveur
    asyncio.create_task(monitor_button())  # Surveille le bouton
    
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
