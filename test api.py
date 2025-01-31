import network
from time import *
import urequests as requests
from picoder import *

led1 = LED(1)
led2 = LED(2)
bzrtone = BUZZRTONE()

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
        
        led1.on()
        led2.on()
        res = requests.get(url='https://api.open-meteo.com/v1/forecast?latitude=46.197376&longitude=5.223058&current=temperature_2m,precipitation&hourly=temperature_2m,precipitation,wind_speed_10m&timezone=auto')
        print(res.text)
        time.sleep(3)
        led1.off()
        led2.off()
        break
        
    elif wlan.status() < 0 or wlan.status() >= 3:
        for i in range(3):
            led1.on()
            sleep(0.01)
            led2.off()
            sleep(0.01)
            bzrtone.play(50,5000)
            sleep(0.01)