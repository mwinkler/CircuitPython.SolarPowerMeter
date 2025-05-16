import random

class HomeAssistant:
    def connect_wifi(self):
        pass

    def get_data(self):
        return {
            "battery_level": random.randint(0, 100),
            "inverter_output": random.randint(0, 2000),
            "grid_power": random.randint(-1000, 3000)
        }