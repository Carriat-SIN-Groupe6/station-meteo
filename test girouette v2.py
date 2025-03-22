from machine import ADC, Pin
import time

# Initialisation du capteur sur la broche GP27 pour Raspberry Pi Pico (PiCoder)
sensor = ADC(27)  # Utilisation directe du canal ADC sur PiCoder

# Dictionnaire des correspondances entre les résistances et les directions du vent
resistance = {
    (32000, 35000): "Nord",
    (6000, 7000): "Nord-Nord-Est",
    (8000, 9000): "Nord-Est",
    (800, 1000): "Est-Nord-Est",
    (900, 1100): "Est",
    (600, 700): "Est-Sud-Est",
    (2000, 2300): "Sud-Est",
    (1400, 1500): "Sud-Sud-Est",
    (3000, 4000): "Sud",
    (3000, 3200): "Sud-Sud-Ouest",
    (15000, 17000): "Sud-Ouest",
    (13000, 15000): "Ouest-Sud-Ouest",
    (100000, 130000): "Ouest",
    (40000, 43000): "Ouest-Nord-Ouest",
    (60000, 66000): "Nord-Ouest",
    (20000, 23000): "Nord-Nord-Ouest"
}

def get_wind_direction(value):
    for (minimum, maximum), direction in resistance.items():
        if minimum <= value <= maximum:
            return direction
    return "Direction inconnue"

while True:
    valeur = sensor.read_u16()  # Lire la valeur ADC sur 16 bits (PiCoder)
    print(f"Valeur lue : {valeur} - Direction du vent : {get_wind_direction(valeur)}")
    time.sleep(1)
