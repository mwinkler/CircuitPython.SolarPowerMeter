import displayio
import adafruit_imageload
from adafruit_display_text import label

class UiElement:
    def __init__(self, container: displayio.Group, image: str=None, x: int=0, y: int=0, font: object=None, hidden: bool=False):
        # init ui group
        self._group = displayio.Group(x=x, y=y)
        self._group.hidden = hidden
        container.append(self._group)

        # image
        image, palette = adafruit_imageload.load(image, bitmap=displayio.Bitmap, palette=displayio.Palette)
        image_tile = displayio.TileGrid(image, pixel_shader=palette, x=46, y=0)
        self._group.append(image_tile)

        # text
        self._text_tile = label.Label(font, color=0xFFFFFF, anchor_point=(1.0, 0.0), anchored_position=(43, 2), scale=2)
        self._group.append(self._text_tile)

    def update_text(self, text: str, color: int = 0xFFFFFF):
        self._text_tile.color = color
        self._text_tile.text = text

    def hidden(self, hidden: bool):
        self._group.hidden = hidden