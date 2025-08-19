import typing

import skia

from ..resource import SColor, dark_theme, default_font
from .textframe import STextFrame, tpos


class SButton(STextFrame):

    _instances = 0

    def __init__(
        self,
        *args,
        name: str = "SButton",
        size: tuple[tpos, tpos] = (105, 35),
        text: typing.Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, widgetname=name, size=size, text=text, **kwargs)

        self.id = self._name + "." + str(self._instances)
        self._instances += 1
        self.focus = False

        # TODO: implement callable funcitons
        self.bind_event(self.id, "mouse_press", self._on_press)
        self.bind_event(self.id, "mouse_release", self._on_release)

        # self._on_release()

    def _on_press(self, _) -> None:
        """Handle if widget is pressed"""
        if self.focus:
            self.update_theme(self.focused)

    def _on_release(self, _) -> None:
        """Handle if widget is released"""
        if self.focus:
            self.update_theme(self.normal)
