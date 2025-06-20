import displayio
from adafruit_display_text import label
from solar_display.ui_image import UiImage
from solar_display.ui_base import UiBase

class UiElement(UiBase):
    def __init__(self, container: displayio.Group, image: str=None, x: int=0, y: int=0, font: object=None, hidden: bool=False):
        UiBase.__init__(self, container, x=x, y=y, hidden=hidden)

        # image
        UiImage(self._group, image, 46, 0)

        # text
        self._text_tile = label.Label(font, color=0xFFFFFF, anchor_point=(1.0, 0.0), anchored_position=(43, 2), scale=2)
        self._group.append(self._text_tile)

    def update_text(self, text: str, color: int = 0xFFFFFF):
        self._text_tile.color = color
        self._text_tile.text = text