from os import getenv
import time
from ha import HomeAssistant
from hafake import HomeAssistantFake
from ui import Ui
from wificonnection import Wifi
from adafruit_matrixportal.matrix import Matrix

refresh_rate = 60
dev = True

# init
matrix = Matrix(width=32, height=32, bit_depth=4)
wifi = Wifi(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
ha = HomeAssistantFake() if dev else HomeAssistant(wifi, getenv('HOMEASSISTANT_URL'), getenv('HOMEASSISTANT_TOKEN'))
ui = Ui(matrix)

# start
ui.init()
#wifi.connect()

# app loop
while True:
    # load data
    data = ha.get_data()

    # display data
    ui.update(data)

    # for i in range(100):
    #     ui.draw_battery_state(i)
    #     time.sleep(0.1)
    time.sleep(5 if dev else refresh_rate)

