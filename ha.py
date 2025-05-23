from wificonnection import Wifi

state_battery_level = "sensor.batteries_state_of_capacity"
state_battery_charge_discharge_power = "sensor.batteries_charge_discharge_power"
state_inverter_output = "sensor.inverter_input_power"
state_grid_power = "sensor.power_meter_active_power"
state_house_consumption = "sensor.shellypro3em_e05a1b334ed4_total_active_power"

class HomeAssistant:
    def __init__(self, wifi: Wifi, url: str, token: str):
        self.url = url
        self.token = token
        self.wifi = wifi

    def _fetch_state(self, entity_id):
        print("Fetching state for entity:", entity_id)
        url = f"{self.url}/api/states/{entity_id}"
        headers = { "Authorization": f"Bearer {self.token}" }
        session = self.wifi.get_session()
        for attempt in range(3):
            try:
                r = session.get(url, headers=headers)
                data = r.json()
                #print("State data:", data)
                return data["state"]
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    return None

    def _get_battery_level(self):
        data = self._fetch_state(state_battery_level)
        print(f"Battery level {data}%")
        return data

    def _get_inverter_output(self):
        data = self._fetch_state(state_inverter_output)
        print(f"Inverter output {data}W")
        return data

    def _get_grid_power(self):
        data = self._fetch_state(state_grid_power)
        print(f"Grid power {data}W")
        return data
    
    def _get_battery_charge_discharge_power(self):
        data = self._fetch_state(state_battery_charge_discharge_power)
        print(f"Battery charge/discharge power {data}W")
        return data
    
    def _get_house_consumption(self):
        data = self._fetch_state(state_house_consumption)
        print(f"House consumption {data}W")
        return data
    
    def get_data(self):
        data = {
            "battery_level": self._get_battery_level(),
            "battery_charge_discharge_power": self._get_battery_charge_discharge_power(),
            "inverter_output": self._get_inverter_output(),
            "grid_power": self._get_grid_power(),
            "house_consumption": self._get_house_consumption()
        }
        return data