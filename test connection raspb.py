import network
from time import *

#Entrer les paramètres du point d'accès
ssid = 'WIFI-SIN'
password = '12345678'

#Connexion au point d'accès
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140)              # désactive le mode power-save
wlan.connect(ssid, password)

# Attente connexion ou erreur de connexion
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Attente connexion...')
    sleep(1)

# Gestion erreur de connexion
if wlan.status() != 3:
    raise RuntimeError('Echec connexion')
else:
    print('Connexion reussie')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )


