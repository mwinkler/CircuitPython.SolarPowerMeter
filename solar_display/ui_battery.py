import displayio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from solar_display.ui_image import UiImage
from solar_display.ui_base import UiBase
from solar_display.ha_data import HaData

class UiBattery(UiBase):
    def __init__(self, container: displayio.Group, x: int, y: int, font: object, hidden: bool=False):
        UiBase.__init__(self, container, x=x, y=y, hidden=hidden)

        # battery image
        UiImage(self._group, "assets/bat.png", 0, 0)

        # text
        self._level_text = label.Label(font, color=0xFFFFFF, anchor_point=(1.0, 0.0), anchored_position=(62, 0), scale=2)
        self._group.append(self._level_text)

        # progress bar
        self._level_bar_group = displayio.Group()
        self._group.append(self._level_bar_group)

        # drain blinker
        self._drain_blinker = Rect(2, 2, 1, 6, fill=0x0)
        self._group.append(self._drain_blinker)

        # charge image
        self._charge_image = UiImage(self._group, "assets/bat_charge_2.png", 7, -1, hidden=True)

    def update(self, data: HaData):
        self._level_text.text = f"{data.battery_level}%"

        # clear previous battery level bar
        try:
            self._level_bar_group.pop()
        except:
            pass
        
        # set color by level
        color = 0x00FF00
        if data.battery_level >= 40:
            color = 0x00FF00
        elif data.battery_level >= 20:
            color = 0xFFFF00
        # elif battery_level >= 20:
        #     color = 0xFFA500
        else:
            color = 0xFF0000
        
        # draw battery level bar
        level_width = min(max(int(data.battery_level // 5.1), 1), 18)
        battery_level_bar = Rect(2, 2, level_width, 6, fill=color)
        self._level_bar_group.append(battery_level_bar)

        # show drain blinker if discharging
        self._drain_blinker.x = level_width + 1
        self._drain_blinker.fill = color if data.battery_charge_discharge_rate > -10 or self._drain_blinker.fill == 0x0 else 0x0
        
        # show charge image if charging
        self._charge_image.show(data.battery_charge_discharge_rate > 10)