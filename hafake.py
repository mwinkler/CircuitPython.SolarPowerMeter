import random

class HomeAssistant:
    def connect_wifi(self):
        pass

    def get_data(self):
        return {
            "battery_level": random.randint(0, 100),
            "battery_charge_discharge_power": random.randint(-2000, 2000),
            "inverter_output": random.randint(0, 2000),
            "grid_power": random.randint(-1000, 3000),
            "house_consumption": random.randint(0, 8000)
        }