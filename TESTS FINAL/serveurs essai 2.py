import network
import socket
import uasyncio as asyncio
import json
from machine import ADC, Pin
from picoder import LEDMATRIX, BUZZERTONE, BUTTON, LCD, BME280
import sys

# Sensor Initialization
bme280 = BME280()
sensor = ADC(27)
wind_direction_state = ""
btn4 = BUTTON(4)

# WiFi Configuration
SSID = 'WIFI-SIN'
PASSWORD = '12345678'

# Server Configuration
HTTP_PORT = 80
WS_PORT = 12345
HOST = "0.0.0.0"

# Wind Direction Resistance Mapping
WIND_DIRECTION_MAP = {
    (49000, 51000): "Nord",
    (5000, 7000): "Est",
    (17000, 19000): "Sud",
    (59000, 61000): "Ouest",
}

def get_wind_direction(value):
    """Determine wind direction based on sensor value"""
    global wind_direction_state
    for (minimum, maximum), direction in WIND_DIRECTION_MAP.items():
        if minimum <= value <= maximum:
            wind_direction_state = direction
            return direction
    
    return wind_direction_state or "Unknown"

def get_weather_data():
    """Collect and return weather sensor data"""

    try:
        return {
            "temperature": bme280.temperature(),
            "humidity": bme280.humidity(),
            "pressure": bme280.pressure(),
            "wind_direction": get_wind_direction(sensor.read_u16())
        }
    except Exception as e:
        print(f"Sensor error: {e}")
        return {
            "temperature": None,
            "humidity": None,
            "pressure": None,
            "wind_direction": "Error"
        }

async def connect_wifi():
    """Establish WiFi connection"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() in (network.STAT_GOT_IP, network.STAT_IDLE):
            break
        max_wait -= 1
        print('Connecting...')
        await asyncio.sleep(1)

    if wlan.status() != network.STAT_GOT_IP:
        print('Connection Failed')
        return False
    else:
        print('Connected, IP:', wlan.ifconfig()[0])
        return True

async def handle_http(reader, writer):
    """Simple HTTP server to serve HTML page"""
    try:
        # Read the request
        request = await reader.read(1024)
        
        # Serve HTML content
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        with open("index copy.html", "r") as file:
            response += file.read()
        
        writer.write(response.encode())
        await writer.drain()
        writer.close()
    except Exception as e:
        print(f"HTTP Server Error: {e}")

async def websocket_handler(reader, writer):
    """WebSocket data streaming handler"""
    try:
        while True:
            # Prepare weather data
            weather_data = json.dumps(get_weather_data())
            
            # Send data
            writer.write(weather_data.encode())
            await writer.drain()
            
            # Wait before next update
            await asyncio.sleep(2)
    except Exception as e:
        print(f"WebSocket Error: {e}")
        try:
            if btn4.read()==1:
                writer.close()
        except:
            pass

async def shutdown_button():
    """Check for shutdown button press"""
    while True:
        if btn4.read() == 1:
            print("\nArrêt du serveur.")
            sys.exit()
        await asyncio.sleep(0.1)

async def main():
    """Main async function to coordinate servers"""
    # Connect to WiFi
    if not await connect_wifi():
        return

    # Start HTTP server
    try:
        http_server = await asyncio.start_server(handle_http, HOST, HTTP_PORT)
        print(f"HTTP Server started on port {HTTP_PORT}")
    except Exception as e:
        print(f"Failed to start HTTP server: {e}")

    # Start WebSocket server
    try:
        ws_server = await asyncio.start_server(websocket_handler, HOST, WS_PORT)
        print(f"WebSocket Server started on port {WS_PORT}")
    except Exception as e:
        print(f"Failed to start WebSocket server: {e}")

    # Keep the program running
    while True:
        await shutdown_button()
        await asyncio.sleep(1)

# Run the main async function
asyncio.run(main())