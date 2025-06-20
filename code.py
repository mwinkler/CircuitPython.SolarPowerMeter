import rgbmatrix
import framebufferio
import board
import displayio
import asyncio
from os import getenv
from solar_display.ha import HomeAssistant
from solar_display.ha_fake import HomeAssistantFake
from solar_display.ui import Ui
from solar_display.mqtt import MqttConnector

# settings
dev = False
refresh_rate = 2 if dev else 60

# init
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=64, bit_depth=4,
    rgb_pins=[board.MTX_R1, board.MTX_G1, board.MTX_B1, board.MTX_R2, board.MTX_G2, board.MTX_B2],
    addr_pins=[board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD, board.MTX_ADDRE],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE,
    doublebuffer=True)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)
ha = HomeAssistantFake() if dev else HomeAssistant(getenv('HOMEASSISTANT_URL'), getenv('HOMEASSISTANT_TOKEN'))
ui = Ui(display)
mqtt = MqttConnector(getenv("MQTT_BROKER"), getenv("MQTT_USERNAME"), getenv("MQTT_PASSWORD"))

def mqtt_callback(message):
    print(f"MQTT message received: {message}")

# app loop
async def main():
    mqtt.subscribe("zigbee2mqtt/Cube1", mqtt_callback)

    while True:
        try:
            # load data
            data = await ha.get_data()

            # update mqtt
            mqtt.poll()

            # display data
            ui.update(data)

        except Exception as e:
            print(f"Error: {e}")

        # wait
        await asyncio.sleep(refresh_rate)

# run app
asyncio.run(main())