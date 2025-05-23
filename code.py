from os import getenv
import time
from ha import HomeAssistant
from hafake import HomeAssistantFake
from ui import Ui
from wifi import Wifi

refresh_rate = 60
dev = True

# init
print("Starting...")

wifi = Wifi(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
ui = Ui()

ui.init()
session = None if dev else wifi.connect()
ha = HomeAssistantFake() if dev else HomeAssistant(session, getenv('HOMEASSISTANT_URL'), getenv('HOMEASSISTANT_TOKEN'))

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
