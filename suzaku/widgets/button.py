import typing

import skia

from ..resource import SColor, default_font
from .textframe import STextFrame, tpos


class SButton(STextFrame):
    def __init__(
        self,
        *args,
        name: str = "SButton",
        size: tuple[tpos, tpos] = (105, 35),
        text: typing.Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, widgetname=name, size=size, text=text, **kwargs)

        self._name = widgetname = "SButton"
        self.id = self._name + "." + str(self._instances)
        self._instances += 1
        self.focus = False

        # TODO: implement event
        # TODO: implement callable funcitons
        self.bind_event(self.id, "mouse_press", self.press)
        self.bind_event(self.id, "mouse_release", self.release)

    def check_focus(self) -> None:
        return self.focus

    def press(self, *args, **kwargs) -> None:
        if self.check_focus():
            self.bd = self.bg = SColor([112, 110, 170]).color

    def release(self, *args, **kwargs) -> None:
        if self.check_focus():
            self.bg = SColor([33, 33, 33, 235]).color
            self.bd = SColor([43, 43, 43, 235]).color
