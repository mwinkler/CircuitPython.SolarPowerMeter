import displayio
import adafruit_imageload

class UiImage:
    def __init__(self, container: displayio.Group, image_path: str, x: int=0, y: int=0, hidden: bool=False):
        image, palette = adafruit_imageload.load(image_path, bitmap=displayio.Bitmap, palette=displayio.Palette)
        self._image_tile = displayio.TileGrid(image, pixel_shader=palette, x=x, y=y)
        self._image_tile.hidden = hidden
        container.append(self._image_tile)
    
    def show(self, show: bool=True):
        self._image_tile.hidden = not show
        

    