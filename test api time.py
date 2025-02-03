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

        res = requests.get(url='https://api.open-meteo.com/v1/forecast?latitude=46.197376&longitude=5.223058&current=temperature_2m,apparent_temperature,precipitation,wind_speed_10m&timezone=Europe%2FLondon')
        ledmatrix.on((0,255,0),0.02)
        bzrtone.play(523,5000)
        sleep(0.5)
        bzrtone.play(659,5000)
        sleep(0.5)
        bzrtone.play(880,5000)
        sleep(1)
        bzrtone.stop()
        res_json = res.json()
        print(f"Il fait {res_json["current"]["apparent_temperature"]} degres Celcius, Il pleut actuellement a {res_json["current"]["precipitation"]} mm.")
        print(f"Il souffle dehors a {res_json["current"]["wind_speed_10m"]} km/h, a Bourg-En-Bresse.")  
        ledmatrix.off()
        time.sleep(3)
        break
        
    elif wlan.status() < 0 or wlan.status() >= 3:
        for i in range(3):
            ledmatrix.on((255,0,0),0.02)
            bzrtone.play(50,5000)
            sleep(1)
            ledmatrix.off()
            break