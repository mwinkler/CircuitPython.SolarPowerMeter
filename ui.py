import displayio
from adafruit_matrixportal.matrix import Matrix
from adafruit_bitmap_font import bitmap_font
from uibattery import UiBattery
from uielement import UiElement

# settings
left_offset = 1
text_offset = 9

class Ui:
    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        
        # init root group
        matrix.display.root_group = displayio.Group()

        # load font
        font = bitmap_font.load_font("assets/04B_03__6pt.pcf", displayio.Bitmap)
        
        # init elements
        #battery_level_text.text = "load"
        self.battery_ui = UiBattery(matrix.display.root_group, left_offset, 1, font, True)
        self.grid_power_ui = UiElement(matrix.display.root_group, "assets/grid.bmp", left_offset, 7, text_offset, 3, font, True)
        self.inverter_ui = UiElement(matrix.display.root_group, "assets/sun.bmp", left_offset, 15, text_offset, 3, font, True)
        self.house_ui = UiElement(matrix.display.root_group, "assets/home.bmp", left_offset, 23, text_offset, 3, font, True)
        self.loader = UiElement(matrix.display.root_group, "assets/flash.png", font=font)

    def hide_loader(self):
        # hide loader
        self.loader.group.hidden = True

        # show elements
        self.battery_ui.group.hidden = False
        self.grid_power_ui.group.hidden = False
        self.inverter_ui.group.hidden = False
        self.house_ui.group.hidden = False

    def update(self, data):
        # disable auto refresh to avoid flickering
        self.matrix.display.auto_refresh = False

        # hide loader
        self.hide_loader()

        # battery level
        self.battery_ui.update_level(data["battery_level"])

        # grid power
        if data["grid_power"] is not None:
            grid_power = int(data["grid_power"])
            self.grid_power_ui.update_text(f"{abs(grid_power)}", 0xFFFFFF if grid_power >= 0 else 0xFF0000)

        # inverter output
        self.inverter_ui.update_text(f"{data["inverter_output"]}")

        # house consumption
        if data["house_consumption"] is not None:
            self.house_ui.update_text(f"{int(float(data["house_consumption"]))}")

        # update the display
        self.matrix.display.auto_refresh = True