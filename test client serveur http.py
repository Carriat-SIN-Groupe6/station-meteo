import network, socket, time
import uasyncio as asyncio
from time import sleep
from picoder import *

led = LED(1),LED(2)
btn1 = BUTTON(1)
display = LCD()

# paramètres du réseau local
ssid = 'WIFI-SIN'
password = '12345678'

wlan = network.WLAN(network.STA_IF)

""" Gère la connexion au réseau local
"""
wlan.active(True)
wlan.config(pm = 0xa11140) # Disable power-save mode
wlan.connect(ssid, password)


max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('veuillez patienter...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('connexion echoue')
else:
    print('connexion reussie')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
    
    
# Configuration du serveur
HOST = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
PORT = 80         # Port HTTP

# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Serveur HTTP en attente de connexion sur le port {PORT}...")

# Page JSON à envoyer
json = """\
HTTP/1.1 200 OK
Content-Type: application/json

{"test":1}
"""

while True:
    conn, addr = server_socket.accept()
    print(f"Connexion de {addr}")

    # Lire la requête HTTP du client
    request = conn.recv(1024)
    print("Requête reçue:", request.decode())

    # Envoyer la réponse HTTP avec la page JSON
    conn.sendall(json.encode())

    # Fermer la connexion
    conn.close()
