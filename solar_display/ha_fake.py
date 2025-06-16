import random

class HomeAssistantFake:
    def __init__(self):
        self.bat = 100

    def get_data(self):
        self.bat = self.bat - 5 if self.bat > 0 else 100
        return {
            "battery_level": self.bat,
            "battery_charge_discharge_power": random.randint(-2000, 2000),
            "inverter_output": random.randint(0, 2000),
            "grid_power": random.randint(-1000, 3000),
            "house_consumption": random.randint(0, 8000)
        }