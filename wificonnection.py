import adafruit_requests
import adafruit_connection_manager
import adafruit_requests
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi

class Wifi:
    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        
        esp32_cs = DigitalInOut(board.ESP_CS)
        esp32_ready = DigitalInOut(board.ESP_BUSY)
        esp32_reset = DigitalInOut(board.ESP_RESET)

        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

        pool = adafruit_connection_manager.get_radio_socketpool(self.esp)
        ssl_context = adafruit_connection_manager.get_radio_ssl_context(self.esp)
        self.session = adafruit_requests.Session(pool, ssl_context)

    def connect(self):
        print("Firmware vers.", self.esp.firmware_version)
        print("Connecting to AP...")
        
        while not self.esp.is_connected:
            try:
                self.esp.connect_AP(self.ssid, self.password)
            except OSError as e:
                print("could not connect to AP, retrying: ", e)
                continue

        print("Connected to", self.esp.ap_info.ssid, "\tRSSI:", self.esp.ap_info.rssi)
        print("My IP address is", self.esp.ipv4_address)
    
    def get_session(self) -> adafruit_requests.Session:
        if self.esp.status != adafruit_esp32spi.WL_CONNECTED:
            print("ESP32 not connected, reconnecting...")
            self.connect()

        return self.session