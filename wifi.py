import adafruit_requests
import adafruit_connection_manager
import adafruit_requests
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
session = adafruit_requests.Session(pool, ssl_context)


class Wifi:
    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password

    def connect(self) -> adafruit_requests.Session:
        if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("ESP32 found and in idle mode")
        print("Firmware vers.", esp.firmware_version)

        print("Connecting to AP...")
        while not esp.is_connected:
            try:
                esp.connect_AP(self.ssid, self.password)
            except OSError as e:
                print("could not connect to AP, retrying: ", e)
                continue
        print("Connected to", esp.ap_info.ssid, "\tRSSI:", esp.ap_info.rssi)
        print("My IP address is", esp.ipv4_address)

        return session