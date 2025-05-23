import displayio
import adafruit_imageload
from adafruit_display_text import label

class UiElement:
    def __init__(self, container: displayio.Group, image: str, x: int, y: int, text_x: int, text_y: int, font: object):
        # init ui group
        group = displayio.Group(x=x, y=y)
        container.append(group)

        # image
        image, palette = adafruit_imageload.load(image, bitmap=displayio.Bitmap, palette=displayio.Palette)
        image_tile = displayio.TileGrid(image, pixel_shader=palette, x=0, y=0)
        group.append(image_tile)

        # text
        self.text_tile = label.Label(font, color=0xFFFFFF, x=text_x, y=text_y)
        group.append(self.text_tile)

    def update_text(self, text: str, color: int = 0xFFFFFF):
        self.text_tile.color = color
        self.text_tile.text = text