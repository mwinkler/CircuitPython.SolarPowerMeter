import time
from os import getenv
from ha import HomeAssistant
from hafake import HomeAssistantFake
from ui import Ui
from wificonnection import Wifi
from adafruit_matrixportal.matrix import Matrix

refresh_rate = 60
dev = False

# init
matrix = Matrix(width=32, height=32, bit_depth=4)
wifi = Wifi(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
ha = HomeAssistantFake() if dev else HomeAssistant(wifi, getenv('HOMEASSISTANT_URL'), getenv('HOMEASSISTANT_TOKEN'))
ui = Ui(matrix)

# app loop
while True:
    # load data
    data = ha.get_data()

    # display data
    ui.update(data)

    # wait
    time.sleep(5 if dev else refresh_rate)