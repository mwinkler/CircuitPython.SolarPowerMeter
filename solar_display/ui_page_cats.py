import displayio
from solar_display.ui_image import UiImage
from solar_display.ui_base import UiBase

class UiPageCats(UiBase):
    def __init__(self, container: displayio.Group):
        UiBase.__init__(self, container, hidden=True)

        UiImage(self._group, "assets/cat_tigi.png", 1, 1)
        UiImage(self._group, "assets/cat_tinka.png", 20, 1)

    

    