import displayio
import adafruit_imageload

class UiImage:
    def __init__(self, container: displayio.Group, image_path: str, x: int=0, y: int=0):
        image, palette = adafruit_imageload.load(image_path, bitmap=displayio.Bitmap, palette=displayio.Palette)
        self._image_tile = displayio.TileGrid(image, pixel_shader=palette, x=x, y=y)
        container.append(self._image_tile)
    
    def show(self, hidden: bool=False):
        self._image_tile.hidden = hidden
        

    