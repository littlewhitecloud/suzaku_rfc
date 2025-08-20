import typing

import skia

from .textframe import STextFrame, tpos


class SLabel(STextFrame):
    def __init__(
        self,
        *args,
        name: str = "SLabel",
        size: tuple[tpos, tpos] = (50, 0),
        text: typing.Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, widgetname=name, size=size, text=text, **kwargs)
        # TODO: size(0, 0) seems don't draw anything but it would be bad when calculating size

        self.layoutconfig["x"] += size[0]
        # self.layoutconfig["x"] += self._text_draw_x
        # self.layoutconfig["y"] += self._text_draw_y

        self.width = 0
        self.height = 0

    def _draw_border(self, _: skia.Surface, __: skia.Rect) -> None:
        """SLabel don't need to draw border"""
        ...

    def draw(self, canvas) -> None:
        self._draw(canvas)
