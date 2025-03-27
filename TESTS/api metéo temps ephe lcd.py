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
        res_météo = requests.get(url='https://api.open-meteo.com/v1/forecast?latitude=46.19737&longitude=5.22305&current=apparent_temperature,precipitation,wind_speed_10m&timezone=auto&forecast_days=1')
        
        ledmatrix.on((0,255,0),0.02)
        
        bzrtone.play(523,5000)
        sleep(0.5)
        bzrtone.play(659,5000)
        sleep(0.5)
        bzrtone.play(880,5000)
        sleep(1)
        bzrtone.stop()
        
        resmétéo_json = res_météo.json()
        res_ephe_json = res_ephe.json()
        
        print('\n-------------------------------------------------------------------------------------------------------------------')
        print(f"Il fait {resmétéo_json["current"]["apparent_temperature"]} degres Celcius, Il pleut actuellement a {resmétéo_json["current"]["precipitation"]} mm.")
        print(f"Il souffle dehors a {resmétéo_json["current"]["wind_speed_10m"]} km/h, a Bourg-En-Bresse.")  
        print('\n-------------------------------------------------------------------------------------------------------------------')
        print(f"Le soleil va se coucher a {res_ephe_json['results']["sunset"]}.")
        print(f"Le soleil va se lever a {res_ephe_json['results']["sunrise"]} .")
        
        time.sleep(3)
        break
        
        
        
    elif wlan.status() < 0 or wlan.status() >= 3:
        for i in range(3):
            
            ledmatrix.on((255,0,0),0.02)
            
            bzrtone.play(523,5000)
            sleep(0.5)
            bzrtone.play(659,5000)
            sleep(0.5)
            bzrtone.play(880,5000)
            sleep(1)
            bzrtone.play(50,5000)
            sleep(0.01)
            bzrtone.stop()
            
            ledmatrix.off()
            
            time.sleep(2)
            
            break
        
        