import network
from time import *
import urequests as requests
from picoder import *

ledmatrix = LEDMATRIX()
bzrtone = BUZZERTONE()
btn1 = BUTTON(1)
btn2 = BUTTON(2)
btn3 = BUTTON(3)
display = LCD()




ledmatrix.off()

#Entrer les paramètres du point d'accès
ssid = 'WIFI-SIN'
password = '12345678'

#Connexion au point d'accès
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140)              # désactive le mode power-save
wlan.connect(ssid, password)


def menu():
    display.draw_text8x8(1, 210, "BTN1 = EPHEMERIDE",RGB(255, 0, 0))
    display.draw_text8x8(1, 225, "BTN2 = METEO",RGB(0, 255, 0))
    display.draw_text8x8(117, 225, "BTN3 = TIME",RGB(0, 0, 255))



menu()

while True:
    valbtn1 = btn1.read()
    valbtn2 = btn2.read()
    valbtn3 = btn3.read()
    menu()
    

    if wlan.status() == 3 and valbtn1==1 :
        display.clear()
        menu()
        
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

        display.draw_text8x8(0, 35, f"Le soleil va se lever a {res_ephe_json['results']["sunrise"]} .",RGB(255, 255, 255))
        display.draw_text8x8(0, 20, f"Le soleil va se coucher a {res_ephe_json['results']["sunset"]}.",RGB(255, 255, 255))
        

        
        
    
    
    if wlan.status() == 3 and valbtn2==1 :
        display.clear()
        menu()
        
        res_météo = requests.get(url='https://api.open-meteo.com/v1/forecast?latitude=46.19737&longitude=5.22305&current=apparent_temperature,precipitation,wind_speed_10m&timezone=auto&forecast_days=1')
        resmétéo_json = res_météo.json()
        
        ledmatrix.on((0,255,0),0.02)
        
        bzrtone.play(1024,5000)
        sleep(0.5)
        bzrtone.play(2048,5000)
        sleep(0.5)
        bzrtone.play(4096,5000)
        sleep(1)
        bzrtone.stop()
        
        ledmatrix.off()
        
        resmétéo_json = res_météo.json()

        display.draw_text8x8(0, 20, f"Il fait {resmétéo_json["current"]["apparent_temperature"]} degres",RGB(255, 255, 255))
        display.draw_text8x8(0, 35, f"Il pleut actuellement a {resmétéo_json["current"]["precipitation"]} mm.",RGB(255, 255, 255))
        display.draw_text8x8(0, 50, f"Il souffle dehors a {resmétéo_json["current"]["wind_speed_10m"]} km/h.",RGB(255, 255, 255))

    
    if wlan.status() == 3 and valbtn3==1 :
        display.clear()
        menu()
        
        res_time = requests.get(url='https://timeapi.io/api/time/current/zone?timeZone=Europe%2FParis')
        restime_json = res_time.json()
        
        ledmatrix.on((0,255,0),0.02)
        
        bzrtone.play(256,5000)
        sleep(0.5)
        bzrtone.play(512,5000)
        sleep(0.5)
        bzrtone.play(1024,5000)
        sleep(1)
        bzrtone.stop()
        
        ledmatrix.off()
        
        restime_json = res_time.json()
        
        display.draw_text8x8(0, 20, f"We are {restime_json["dayOfWeek"]} {restime_json["date"]}",RGB(255, 255, 255))
        display.draw_text8x8(0, 35, f"This is {restime_json["time"]}:{restime_json["seconds"]} .",RGB(255, 255, 255))        
