import adafruit_requests
from os import getenv
import adafruit_connection_manager
import adafruit_requests
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi

ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
requests = adafruit_requests.Session(pool, ssl_context)

#esp._debug = True

class HomeAssistant:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def connect_wifi(self):
        if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("ESP32 found and in idle mode")
        print("Firmware vers.", esp.firmware_version)

        print("Connecting to AP...")
        while not esp.is_connected:
            try:
                esp.connect_AP(ssid, password)
            except OSError as e:
                print("could not connect to AP, retrying: ", e)
                continue
        print("Connected to", esp.ap_info.ssid, "\tRSSI:", esp.ap_info.rssi)
        print("My IP address is", esp.ipv4_address)

    def _fetch_state(self, entity_id):
        print("Fetching state for entity: ", entity_id)
        url = f"{self.url}/api/states/{entity_id}"
        headers = { "Authorization": f"Bearer {self.token}" }
        for attempt in range(3):
            try:
                r = requests.get(url, headers=headers)
                data = r.json()
                #print("State data:", data)
                return data["state"]
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    return None

    def _get_battery_level(self):
        data = self._fetch_state("sensor.batteries_state_of_capacity")
        print(f"Battery level {data}%")
        return data

    def _get_inverter_output(self):
        data = self._fetch_state("sensor.inverter_input_power")
        print(f"Inverter output {data}W")
        return data

    def _get_grid_power(self):
        data = self._fetch_state("sensor.power_meter_active_power")
        print(f"Grid power {data}W")
        return data
    
    def get_data(self):
        data = {
            "battery_level": self._get_battery_level(),
            "inverter_output": self._get_inverter_output(),
            "grid_power": self._get_grid_power()
        }
        return data
    
