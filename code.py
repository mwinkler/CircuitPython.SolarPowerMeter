import time
import ha
import ui

print("Starting...")

# init
ui.init()
#ha.connect_wifi()

# load data
#bat = ha.get_battery_state()

# draw data
#ui.draw_battery_state(bat)
#ui.draw_battery_state(10)

while True:
    for i in range(100):
        ui.draw_battery_state(i)
        time.sleep(0.1)
    time.sleep(2)
