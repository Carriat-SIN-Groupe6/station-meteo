import network, socket, uasyncio as asyncio
from picoder import LED, BUTTON, LCD
import sys

# Initialisation des composants
led = LED(1), LED(2)
btn1 = BUTTON(1)
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
Content-Type: application/json

{"test":1}
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
        if btn1.read() == 1:
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
