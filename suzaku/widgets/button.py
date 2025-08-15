import typing

import skia

from ..resource import SColor, default_font, dark_theme
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
        self.clicked = False

        # TODO: implement callable funcitons
        self.bind_event(self.id, "mouse_press", self._on_press)
        self.bind_event(self.id, "mouse_release", self._on_release)

        self._on_release()


    def check_focus(self) -> None:
        return self.focus and not self.clicked

    def _on_press(self, *args, **kwargs) -> None:
        """Handle if widget is pressed"""
        if self.check_focus():
            self.update_theme(self.normal)
            self.clicked = True

    def _on_release(self, *args, **kwargs) -> None:
        """Handle if widget is released"""
        if not self.check_focus():
            self.update_theme(self.unfocused)
            self.clicked = False
