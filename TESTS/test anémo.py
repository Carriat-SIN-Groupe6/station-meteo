from machine import Pin
import time

# Initialisation des broches
capteur = Pin(14, Pin.IN, Pin.PULL_UP)  # Capteur en entrée avec pull-up activé

while True:
    if capteur.value() == 0:  # Si le capteur est activé (LOW)
        print('1')  # Allume la LED
    else:
        print('0') # Éteint la LED
    time.sleep(0.01)  # Petit délai pour éviter les rebonds
