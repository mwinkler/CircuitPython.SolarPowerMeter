
import displayio
import adafruit_imageload
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

class UiBattery:
    def __init__(self, container: displayio.Group, x: int, y: int, font: object, hidden: bool=False):
        # group
        self.group = displayio.Group(x=x, y=y)
        self.group.hidden = hidden
        container.append(self.group)

        # battery image
        battery_image, palette = adafruit_imageload.load("assets/bat.png", bitmap=displayio.Bitmap, palette=displayio.Palette)
        battery_tile_grid = displayio.TileGrid(battery_image, pixel_shader=palette)
        self.group.append(battery_tile_grid)

        # text
        self.level_text = label.Label(font, color=0xFFFFFF, anchor_point=(1.0, 0.0), anchored_position=(64, 0), scale=2)
        self.group.append(self.level_text)

        # progress bar
        self.level_bar_group = displayio.Group()
        self.group.append(self.level_bar_group)

    def update_level(self, battery_level: str):
        if battery_level is None:
            return

        level_int = int(float(battery_level))
        self.level_text.text = f"{level_int}%"

        # clear previous battery level bar
        try:
            self.level_bar_group.pop()
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
        battery_level_bar = Rect(2, 2, min(max(int(level_int // 5.1), 1), 18), 7, fill=color)
        self.level_bar_group.append(battery_level_bar)

    def hidden(self, hidden: bool):
        self.group.hidden = hidden