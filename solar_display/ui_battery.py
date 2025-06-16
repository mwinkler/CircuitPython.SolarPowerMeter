
import displayio
import adafruit_imageload
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

class UiBattery:
    def __init__(self, container: displayio.Group, x: int, y: int, font: object, hidden: bool=False):
        # group
        self._group = displayio.Group(x=x, y=y)
        self._group.hidden = hidden
        container.append(self._group)

        # battery image
        battery_image, palette = adafruit_imageload.load("assets/bat.png", bitmap=displayio.Bitmap, palette=displayio.Palette)
        battery_tile_grid = displayio.TileGrid(battery_image, pixel_shader=palette)
        self._group.append(battery_tile_grid)

        # text
        self._level_text = label.Label(font, color=0xFFFFFF, anchor_point=(1.0, 0.0), anchored_position=(62, 0), scale=2)
        self._group.append(self._level_text)

        # progress bar
        self._level_bar_group = displayio.Group()
        self._group.append(self._level_bar_group)

    def update_level(self, battery_level: str):
        if battery_level is None:
            return

        level_int = int(float(battery_level))
        self._level_text.text = f"{level_int}%"

        # clear previous battery level bar
        try:
            self._level_bar_group.pop()
        except:
            pass
        
        # set color by level
        color = 0x00FF00
        if level_int >= 40:
            color = 0x00FF00
        elif level_int >= 20:
            color = 0xFFFF00
        # elif battery_level >= 20:
        #     color = 0xFFA500
        else:
            color = 0xFF0000
        
        # draw battery level bar
        battery_level_bar = Rect(2, 2, min(max(int(level_int // 5.1), 1), 18), 6, fill=color)
        self._level_bar_group.append(battery_level_bar)

    def hidden(self, hidden: bool):
        self._group.hidden = hidden