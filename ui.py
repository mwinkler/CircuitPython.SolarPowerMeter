import displayio
from adafruit_matrixportal.matrix import Matrix
from adafruit_bitmap_font import bitmap_font
from uibattery import UiBattery
from uielement import UiElement

# settings
left_offset = 1
text_offset = 9

# create the matrix display
matrix = Matrix(width=32, height=32, bit_depth=4)

# load font
font = bitmap_font.load_font("assets/04B_03__6pt.pcf", displayio.Bitmap)

# init root group
matrix.display.root_group = displayio.Group()

# init elements
battery_ui = UiBattery(matrix.display.root_group, left_offset, 1, font)
grid_power_ui = UiElement(matrix.display.root_group, "assets/grid.bmp", left_offset, 7, text_offset, 3, font)
inverter_ui = UiElement(matrix.display.root_group, "assets/sun.bmp", left_offset, 15, text_offset, 3, font)
house_ui = UiElement(matrix.display.root_group, "assets/home.bmp", left_offset, 23, text_offset, 3, font)

class Ui:

    def init(self):
        #battery_level_text.text = "load"
        pass

    def update(self, data):
        # disable auto refresh to avoid flickering
        matrix.display.auto_refresh = False

        # battery level
        battery_ui.update_level(data["battery_level"])

        # grid power
        if data["grid_power"] is not None:
            grid_power_int = int(data["grid_power"])
            grid_power_ui.update_text(f"{abs(grid_power_int)}", 0xFFFFFF if grid_power_int >= 0 else 0xFF0000)

        # inverter output
        inverter_ui.update_text(f"{data["inverter_output"]}")

        # house consumption
        if data["house_consumption"] is not None:
            house_ui.update_text(f"{int(float(data["house_consumption"]))}")

        # update the display
        matrix.display.auto_refresh = True