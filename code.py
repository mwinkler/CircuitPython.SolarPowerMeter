from os import getenv
import time
from ha import HomeAssistant
#from hafake import HomeAssistant
from ui import Ui
from wifi import Wifi

wifi = Wifi(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
ui = Ui()

print("Starting...")

# init
ui.init()
session = wifi.connect()
ha = HomeAssistant(session, getenv('HOMEASSISTANT_URL'), getenv('HOMEASSISTANT_TOKEN'))

# start app loop
while True:
    # load data
    data = ha.get_data()

    ui.draw_battery_state(data["battery_level"])
    ui.draw_grid_power(data["grid_power"])
    ui.draw_inverter_output(data["inverter_output"])
    ui.draw_house_consumption(data["house_consumption"])

    # for i in range(100):
    #     ui.draw_battery_state(i)
    #     time.sleep(0.1)
    time.sleep(60)

