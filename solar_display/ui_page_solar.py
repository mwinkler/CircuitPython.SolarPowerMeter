import displayio
from adafruit_bitmap_font import bitmap_font
from solar_display.ui_battery import UiBattery
from solar_display.ui_element import UiElement
from solar_display.ui_base import UiBase
from solar_display.ha_data import HaData

left_offset = 2

class UiPageSolar(UiBase):
    def __init__(self, container: displayio.Group):
        UiBase.__init__(self, container, hidden=True)

        # load font
        font = bitmap_font.load_font("assets/04B_03__6pt.pcf", displayio.Bitmap)

        # init ui elements
        self._battery_ui = UiBattery(self._group, left_offset, 2, font)
        self._inverter_ui = UiElement(self._group, "assets/sun2.png", left_offset, 15, font)
        self._house_ui = UiElement(self._group, "assets/home2.png", left_offset, 32, font)
        self._grid_power_ui = UiElement(self._group, "assets/grid.png", left_offset, 48, font)
        
    def update(self, data: HaData):
        if data is None:
            return

        # battery level
        self._battery_ui.update(data)

        # grid power
        self._grid_power_ui.update_text(f"{abs(data.grid_power)}", 0xFFFFFF if data.grid_power >= 0 else 0xFF0000)

        # inverter output
        self._inverter_ui.update_text(f"{data.inverter_output}")

        # house consumption
        self._house_ui.update_text(f"{data.house_consumption}")