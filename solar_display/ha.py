import adafruit_requests
import ssl
import socketpool
import wifi
from solar_display.ha_data import HaData

state_battery_level = "sensor.batteries_state_of_capacity"
state_battery_charge_discharge_power = "sensor.batteries_charge_discharge_power"
state_inverter_output = "sensor.inverter_input_power"
state_grid_power = "sensor.power_meter_active_power"
state_house_consumption = "sensor.shellypro3em_e05a1b334ed4_total_active_power"

class HomeAssistant:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.session = adafruit_requests.Session(socketpool.SocketPool(wifi.radio), ssl.create_default_context())

    async def _fetch_state(self, entity_id):
        print("Fetching state for entity:", entity_id)
        url = f"{self.url}/api/states/{entity_id}"
        headers = { "Authorization": f"Bearer {self.token}" }
        for attempt in range(3):
            try:
                response = self.session.get(url, headers=headers)
                data = response.json()
                print("State for entity", entity_id, ":", data["state"])
                #print("State data:", data)
                return data["state"]
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    return None
                
    async def _fetch_int(self, entity_id):
        data = await self._fetch_state(entity_id)
        if data is not None:
            try:
                return int(float(data))
            except ValueError:
                print(f"Invalid integer value for {entity_id}: {data}")
                return None
        return None

    async def get_data(self):
        return HaData(
            battery_level = await self._fetch_int(state_battery_level),
            battery_charge_discharge_rate = await self._fetch_int(state_battery_charge_discharge_power),
            inverter_output = await self._fetch_int(state_inverter_output),
            grid_power = await self._fetch_int(state_grid_power),
            house_consumption = await self._fetch_int(state_house_consumption)
        )