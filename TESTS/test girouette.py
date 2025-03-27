from machine import ADC, Pin
import time

# Initialisation du capteur sur la broche A1 (GPIO 36 sur ESP32, ou GPIO 26 sur Raspberry Pi Pico)
sensor = ADC(Pin(27))  # Modifier la broche selon la carte utilisée

while True:
    sensor_value = sensor.read_u16()  # Utilisation de read_u16() pour MicroPython
    print(sensor_value)  # Affichage de la valeur sur le terminal série
    time.sleep(1.5)  # Pause de 100 ms
    
    if sensor_value <= 28000 and sensor_value >= 34000:
        print('\n\nSTOP!!!!!!!!!!!!!!!')