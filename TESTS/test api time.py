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

        res = requests.get(url='https://timeapi.io/api/time/current/zone?timeZone=Europe%2FParis')
        ledmatrix.on((0,255,0),0.02)
        bzrtone.play(523,5000)
        sleep(0.5)
        bzrtone.play(659,5000)
        sleep(0.5)
        bzrtone.play(880,5000)
        sleep(1)
        bzrtone.stop()
        ledmatrix.off()
        res_json = res.json()
        print(f"This is {res_json["time"]}:{res_json["seconds"]} .")
        print(f"We are {res_json["dayOfWeek"]} {res_json["date"]} .")
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