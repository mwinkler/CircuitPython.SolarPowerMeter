from os import getenv
import time
#from ha import HomeAssistant
from hafake import HomeAssistant
from ui import Ui

ha = HomeAssistant(getenv('HOMEASSISTANT_URL'), getenv('HOMEASSISTANT_TOKEN'))
ui = Ui()

print("Starting...")

# init
ui.init()
ha.connect_wifi()


# draw data
#ui.draw_battery_state(bat)
#ui.draw_battery_state(10)

while True:
    # load data
    data = ha.get_data()

    ui.draw_battery_state(data["battery_level"])
    ui.draw_grid_power(data["grid_power"])

    # for i in range(100):
    #     ui.draw_battery_state(i)
    #     time.sleep(0.1)
    time.sleep(2)
