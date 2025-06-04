import time
from os import getenv
from ha import HomeAssistant
from hafake import HomeAssistantFake
from ui import Ui
from wificonnection import Wifi
from adafruit_matrixportal.matrix import Matrix

dev = False
refresh_rate = 5 if dev else 60

# init
matrix = Matrix(width=64, height=64)
wifi = Wifi(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
ha = HomeAssistantFake() if dev else HomeAssistant(wifi, getenv('HOMEASSISTANT_URL'), getenv('HOMEASSISTANT_TOKEN'))
ui = Ui(matrix)

# app loop
while True:
    try:
        # load data
        data = ha.get_data()

        # display data
        ui.update(data)
    except Exception as e:
        print(f"Error: {e}")

    # wait
    time.sleep(refresh_rate)