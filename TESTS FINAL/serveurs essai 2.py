import network, socket, uasyncio as asyncio
import json
from time import sleep
from machine import ADC, Pin
from picoder import LEDMATRIX, BUZZERTONE, BUTTON, LCD, BME280
import sys

# Initialisation des capteurs
bme280 = BME280()
sensor = ADC(27)

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
        "wind_direction": "Nord"
    }

# Gestion des requêtes HTTP
async def handle_http(reader, writer):
    request = await reader.read(1024)
    with open("index.html", "r") as file:
        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + file.read()
    await writer.awrite(response.encode())
    await writer.aclose()

# Gestion du serveur WebSocket
async def websocket_server(reader, writer):
    try:
        while True:
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
