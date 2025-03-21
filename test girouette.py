from machine import ADC, Pin
import time

# Initialisation du capteur sur la broche A1 (GPIO 36 sur ESP32, ou GPIO 26 sur Raspberry Pi Pico)
sensor = ADC(Pin(36))  # Modifier la broche selon la carte utilisée

while True:
    sensor_value = sensor.read_u16()  # Utilisation de read_u16() pour MicroPython
    print(sensor_value)  # Affichage de la valeur sur le terminal série
    time.sleep(0.1)  # Pause de 100 ms
