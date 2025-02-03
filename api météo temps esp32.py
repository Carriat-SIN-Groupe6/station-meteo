import network
from time import *
import urequests as requests

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
        
        res_météo = requests.get(url='https://api.open-meteo.com/v1/forecast?latitude=46.197376&longitude=5.223058&current=temperature_2m,apparent_temperature,precipitation,wind_speed_10m&timezone=Europe%2FLondon')
        res_time = requests.get(url='https://timeapi.io/api/time/current/zone?timeZone=Europe%2FParis')
        
        resmétéo_json = res_météo.json()
        res_time_json = res_time.json()
        
        print(f"This is {res_time_json["time"]}:{res_time_json["seconds"]} .")
        print(f"We are {res_time_json["dayOfWeek"]} {res_time_json["date"]} .")
        print(f"Il fait {resmétéo_json["current"]["apparent_temperature"]} degres Celcius, Il pleut actuellement a {resmétéo_json["current"]["precipitation"]} mm.")
        print(f"Il souffle dehors a {resmétéo_json["current"]["wind_speed_10m"]} km/h, a Bourg-En-Bresse.")  
        
        sleep(3)
        break
        
        
        
    elif wlan.status() < 0 or wlan.status() >= 3:
        for i in range(3):
            
            print("WLAN non actif")
            
            break
        
        