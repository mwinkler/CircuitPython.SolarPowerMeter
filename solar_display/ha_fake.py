import random
from solar_display.ha import HaData

class HomeAssistantFake:
    def __init__(self):
        self.bat = 100
        self.bat_rate = -10

    async def get_data(self):
        self.bat = max(min(self.bat + self.bat_rate, 100), 0)
        if self.bat <= 0 or self.bat >= 100:
            self.bat_rate = -self.bat_rate

        return HaData(
            battery_level = self.bat,
            battery_charge_discharge_rate = -1000 if self.bat_rate < 0 else 1000,
            inverter_output = random.randint(0, 2000),
            grid_power = random.randint(-1000, 3000),
            house_consumption = random.randint(0, 8000)
        )