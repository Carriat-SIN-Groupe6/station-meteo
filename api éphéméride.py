import network
from time import *
import urequests as requests
from picoder import *

ledmatrix = LEDMATRIX()
bzrtone = BUZZERTONE()

ledmatrix.off()

#Entrer les paramètres du point d'accès
ssid = 'WIFI-SIN'
password = '12345678'

#Connexion au point d'accès
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140)              # désactive le mode power-save
wlan.connect(ssid, password)

while True:
    if wlan.status() == 3:

        res_ephe = requests.get(url='https://api.sunrisesunset.io/json?lat=46.20574&lng=5.2258')
        ledmatrix.on((0,255,0),0.02)
        bzrtone.play(523,5000)
        sleep(0.5)
        bzrtone.play(659,5000)
        sleep(0.5)
        bzrtone.play(880,5000)
        sleep(1)
        bzrtone.stop()
        ledmatrix.off()
        res_ephe_json = res_ephe.json()
        print(f"Le soleil va se coucher a {res_ephe_json['results']["sunset"]}.")
        print(f"Le soleil va se lever a {res_ephe_json['results']["sunrise"]} .")
        time.sleep(3)
        time.sleep(3)
        break
        
    elif wlan.status() < 0 or wlan.status() >= 3:
        for i in range(3):
            ledmatrix.on((255,0,0),0.02)
            bzrtone.play(50,5000)
            sleep(1)
            ledmatrix.off()
            break