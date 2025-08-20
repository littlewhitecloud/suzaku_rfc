import typing

import skia

from .textframe import STextFrame, tpos


class SLabel(STextFrame):
    def __init__(
        self, *args, name: str = "SLabel", text: typing.Optional[str] = None, **kwargs
    ) -> None:
        super().__init__(*args, widgetname=name, size=(0, 0), text=text, **kwargs)
        # TODO: size(0, 0) seems don't draw anything but it would be bad when calculating size
        # self.layoutconfig["x"] += self._text_draw_x
        # self.layoutconfig["y"] += self._text_draw_y

        self.width = self.height = 0

    def _draw_border(self, _: skia.Surface, __: skia.Rect) -> None:
        """SLabel don't need to draw border"""
        ...

    def _draw(self, _: skia.Surface) -> None:
        self._draw_text(_)

    def draw(self, canvas) -> None:
        self._draw(canvas)
