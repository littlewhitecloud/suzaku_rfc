import typing

import glfw

from .event import SEventHandler

wpos = typing.Optional[int]


class SLayoutManager:
    """
    This is a class for SWidget to config layout option
    Only provide `place` just for now
    """

    def __init__(self) -> None:
        self.layoutconfig = {"layouttype": None, "x": 0, "y": 0, "anchor": "N"}

    def place(
        self, x: wpos = None, y: wpos = None, anchor: typing.Optional[str] = None
    ) -> None:
        self.layoutconfig["layouttype"] = "place"
        match anchor:
            case "NW":
                x = self.parent.x
                y = self.parent.y
                pass
            case "N":
                x = self.parent.x + self.parent.width / 2 - self.width / 2
                y = self.parent.y + self.height
            case "NE":
                x = self.parent.x
                y = self.parent.y + self.parent.width
            case "W":
                x = self.parent.x
                y = self.parent.y + self.parent.height / 2
            case "SW":
                x = self.parent.x
                y = self.parent.y + self.parent.height
            case "S":
                x = self.parent.x + self.parent.width / 2
                y = self.parent.y + self.parent.height
            case "SE":
                x = self.parent.x + self.parent.width - self.width
                y = self.parent.y + self.parent.height
            case "E":
                x = self.parent.x + self.parent.width - self.width
                y = self.parent.y + self.parent.height / 2

        self.layoutconfig["x"] += x
        self.layoutconfig["y"] += (
            y if y == 0 else y - glfw.get_window_frame_size(self.parent.window)[1]
        )

        self.update_layout()


class Calculator:
    """
    This is a class for SContainer to calculate
    The position of the widget by using different layout settings
    And SContainer can inherit this class and calling the functions
    To get the position of the widget on the canvas
    So it can call the `draw()` function of the contained function
    By giving out the (x, y) of the rect of the widget
    Then the widget can draw it correctly
    The position will only calculate once
    And for the further update
    The SWindow will handle it by calling `_on_framebuffered_size()` function
    """

    def __init__(self) -> None: ...

    def calucate_pack(self, widget) -> None: ...


class SContainer(SEventHandler):
    def __init__(self) -> None:
        SEventHandler.__init__(self)
