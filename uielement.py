import displayio
import adafruit_imageload
from adafruit_display_text import label

class UiElement:
    def __init__(self, container: displayio.Group, image: str=None, x: int=0, y: int=0, font: object=None, hidden: bool=False):
        # init ui group
        self.group = displayio.Group(x=x, y=y)
        self.group.hidden = hidden
        container.append(self.group)

        # image
        image, palette = adafruit_imageload.load(image, bitmap=displayio.Bitmap, palette=displayio.Palette)
        image_tile = displayio.TileGrid(image, pixel_shader=palette, x=0, y=0)
        self.group.append(image_tile)

        # text
        self.text_tile = label.Label(font, color=0xFFFFFF, anchor_point=(1.0, 0.0), anchored_position=(62, 2), scale=2)
        self.group.append(self.text_tile)

    def update_text(self, text: str, color: int = 0xFFFFFF):
        self.text_tile.color = color
        self.text_tile.text = text

    def hidden(self, hidden: bool):
        self.group.hidden = hidden