import network, socket, time
import uasyncio as asyncio
import json
from picoder import BME280

# Initialisation des capteurs
bme280 = BME280()

def get_weather_data():
    return {
        "temperature": bme280.temperature(),
        "humidity": bme280.humidity(),
        "pressure": bme280.pressure(),
        "wind_direction": "Nord"  # Remplacez par la vraie valeur si disponible
    }

# Connexion au WiFi
ssid = 'WIFI-SIN'
password = '12345678'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm=0xa11140)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Connexion en cours...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Connexion échouée')
else:
    print('Connexion réussie')
    status = wlan.ifconfig()
    print('IP:', status[0])

# Configuration du serveur WebSocket
HOST = "0.0.0.0"
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Serveur en attente de connexion sur le port {PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"Client connecté depuis {addr}")
    
    try:
        while True:
            weather_data = json.dumps(get_weather_data())
            conn.sendall(weather_data.encode('utf-8'))
            time.sleep(2)
    except Exception as e:
        print(f"Déconnexion du client {addr}: {e}")
    finally:
        conn.close()
