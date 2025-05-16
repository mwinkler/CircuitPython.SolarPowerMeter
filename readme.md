# Solar Power Meter
With Adafruit Portal Matrix M4 and Home Assistant.  
Used firmware `adafruit-circuitpython-matrixportal_m4-en_US-9.2.7`

## Setup
Create `settings.toml`:
```
CIRCUITPY_WIFI_SSID = "[Your WIFI SSID]"
CIRCUITPY_WIFI_PASSWORD = "[Your WIFI password]"
HOMEASSISTANT_URL = "http://[Your Home Assistant url]:60555"
HOMEASSISTANT_TOKEN = "[Long-lived access tokens]"
```