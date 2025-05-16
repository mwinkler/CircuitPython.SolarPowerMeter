import displayio
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text import label
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect

# create the matrix display
matrix = Matrix(width=32, height=32, bit_depth=4)

# load font
font = bitmap_font.load_font("assets/04B_03__6pt.pcf", displayio.Bitmap)

# init root group
matrix.display.root_group = displayio.Group()

# init battery group
battery_group = displayio.Group(x=1, y=1)
matrix.display.root_group.append(battery_group)

# init battery image
battery_image, palette = adafruit_imageload.load(
    "assets/battery.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)
battery_tile_grid = displayio.TileGrid(battery_image, pixel_shader=palette)
battery_group.append(battery_tile_grid)

# init battery level text
battery_level_text = label.Label(font, color=0xFFFFFF, x=14, y=2)
battery_group.append(battery_level_text)

# init battery progress bar
battery_level_bar_group = displayio.Group()
battery_group.append(battery_level_bar_group)

def init():
    battery_level_text.text = "load"

def draw_battery_state(battery_level):
    # disable auto refresh to avoid flickering
    matrix.display.auto_refresh = False

    level_int = int(float(battery_level))
    battery_level_text.text = f"{level_int}%"

    # clear previous battery level bar
    try:
        battery_level_bar_group.pop()
    except:
        pass
    
    # set color by level
    color = 0x00FF00
    if battery_level >= 40:
        color = 0x00FF00
    elif battery_level >= 20:
        color = 0xFFFF00
    # elif battery_level >= 20:
    #     color = 0xFFA500
    else:
        color = 0xFF0000
    
    battery_level_bar = Rect(1, 1, max(int(level_int // 9), 1), 3, fill=color)
    battery_level_bar_group.append(battery_level_bar)

    # update the display
    matrix.display.auto_refresh = True

# export the function
__all__ = ["draw_battery_state", "init"]