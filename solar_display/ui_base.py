import displayio

class UiBase:
    def __init__(self, container: displayio.Group, x: int=0, y: int=0, hidden: bool=False):
        self._group = displayio.Group(x=x, y=y)
        self._group.hidden = hidden
        container.append(self._group)

    def show(self, hidden: bool=False):
        self._group.hidden = hidden