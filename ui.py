import displayio
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text import label
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect

# settings
left_offset = 1

# create the matrix display
matrix = Matrix(width=32, height=32, bit_depth=4)

# load font
font = bitmap_font.load_font("assets/04B_03__6pt.pcf", displayio.Bitmap)

# init root group
matrix.display.root_group = displayio.Group()

# init battery group
battery_group = displayio.Group(x=left_offset, y=1)
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

# init grid power group
grid_power_group = displayio.Group(x=left_offset, y=7)
matrix.display.root_group.append(grid_power_group)

# init battery image
grid_image, palette = adafruit_imageload.load(
    "assets/grid.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)
grid_tile = displayio.TileGrid(grid_image, pixel_shader=palette, x=0, y=0)
grid_power_group.append(grid_tile)

# init grid power text
grid_power_text = label.Label(font, color=0xFFFFFF, x=8, y=3)
grid_power_group.append(grid_power_text)

# init inverter output group
inverter_output_group = displayio.Group(x=left_offset, y=15)
matrix.display.root_group.append(inverter_output_group)

# init inverter output image
inverter_image, palette = adafruit_imageload.load(
    "assets/sun.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)
inverter_tile = displayio.TileGrid(inverter_image, pixel_shader=palette, x=0, y=0)
inverter_output_group.append(inverter_tile)

class Ui:

    def init(self):
        battery_level_text.text = "load"

    def draw_battery_state(self, battery_level):
        if battery_level is None:
            return

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
        if level_int >= 40:
            color = 0x00FF00
        elif level_int >= 20:
            color = 0xFFFF00
        # elif battery_level >= 20:
        #     color = 0xFFA500
        else:
            color = 0xFF0000
        
        battery_level_bar = Rect(1, 1, max(int(level_int // 9), 1), 3, fill=color)
        battery_level_bar_group.append(battery_level_bar)

        # update the display
        matrix.display.auto_refresh = True

    def draw_grid_power(self, grid_power):
        if grid_power is None:
            return

        # disable auto refresh to avoid flickering
        matrix.display.auto_refresh = False

        grid_power_text.color = 0xFFFFFF if grid_power >= 0 else 0xFF0000
        grid_power_text.text = f"{abs(grid_power)}"

        # update the display
        matrix.display.auto_refresh = True

    def draw_inverter_output(self, inverter_output):
        if inverter_output is None:
            return

        # disable auto refresh to avoid flickering
        matrix.display.auto_refresh = False

        inverter_output_text = label.Label(font, color=0xFFFFFF, x=1, y=10)
        inverter_output_text.text = f"{inverter_output}W"
        matrix.display.root_group.append(inverter_output_text)

        # update the display
        matrix.display.auto_refresh = True
