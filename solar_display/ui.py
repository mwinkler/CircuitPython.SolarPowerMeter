import displayio
import framebufferio
from solar_display.ui_page_solar import UiPageSolar
from solar_display.ui_page_test import UiPageTest
from solar_display.ui_page_cats import UiPageCats
from solar_display.ha_data import HaData
from solar_display.ui_image import UiImage

class Ui:
    def __init__(self, framebuffer: framebufferio.FramebufferDisplay):
        self._framebuffer = framebuffer
        
        # init root group
        root_group = displayio.Group()
        framebuffer.root_group = root_group

        # loader
        self._loader = UiImage(root_group, "assets/flash.png", 16, 16)

        # init pages
        self._page_solar = UiPageSolar(root_group)
        self._page_cats = UiPageCats(root_group)
        self._page_test = UiPageTest(root_group)

    def update(self, data: HaData):
        # disable auto refresh to avoid flickering
        self._framebuffer.auto_refresh = False

        # hide loader
        self._loader.show(False)

        # show solar page
        self._page_solar.show()
        #self._page_test.show()
        #self._page_cats.show()

        # update solar page
        self._page_solar.update(data)

        # update the display
        self._framebuffer.auto_refresh = True