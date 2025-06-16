import time
from os import getenv
from solar_display.ha import HomeAssistant
from solar_display.ha_fake import HomeAssistantFake
from solar_display.ui import Ui
import rgbmatrix
import framebufferio
import board
import displayio

# settings
dev = True
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

# app loop
while True:
    try:
        # load data
        data = ha.get_data()

        # display data
        ui.update(data)
    except Exception as e:
        print(f"Error: {e}")

    # wait
    time.sleep(refresh_rate)