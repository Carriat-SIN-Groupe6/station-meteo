import network
from time import *
import urequests as requests
from picoder import *

led1 = LED(1)
led2 = LED(2)

#Entrer les paramètres du point d'accès
ssid = 'WIFI-SIN'
password = '12345678'

#Connexion au point d'accès
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140)              # désactive le mode power-save
wlan.connect(ssid, password)

while True:
    if wlan.status() = 3:
        
        led1.on()
        led2.on()
        res = requests.get(url='http://www.baidu.com/')
        print(res.text)
        time.sleep(3)
        led1.off()
        led2.off()
        
    elif wlan.status() < 0 or wlan.status() >= 3:
        led1.on()
        led2.off()