from machine import ADC, Pin
import time

# Initialisation du capteur sur la broche GP27 pour Raspberry Pi Pico (PiCoder)
sensor = ADC(27)  # Utilisation directe du canal ADC sur PiCoder
etat_direction=0

# Dictionnaire des correspondances entre les résistances et les directions du vent
resistance = {
    (49000, 51000): "Nord",
    (5000, 7000): "Est",
    (17000, 19000): "Sud",
    (59000, 61000): "Ouest",
}


def get_wind_direction(value):
    global etat_direction
    for (minimum, maximum), direction in resistance.items():
        if minimum <= value <= maximum:
            etat_direction=direction
            return direction
        
    return etat_direction

while True:
    valeur = sensor.read_u16()  # Lire la valeur ADC sur 16 bits (PiCoder)
    print(f"Valeur lue : {valeur} - Direction du vent : {get_wind_direction(valeur)}")
    time.sleep(0.2)
