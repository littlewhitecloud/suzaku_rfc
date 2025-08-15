import skia
import typing

from .textframe import STextFrame, tpos
from ..resource import SColor

class SLabel(STextFrame):
    def __init__(
        self,
        *args,
        name: str = "SLabel",
        size: tuple[tpos, tpos] = (105, 35),
        text: typing.Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, widgetname=name, size=size, text=text, **kwargs)

        # TODO: size(0, 0) seems don't draw anything
        self.normal = self.parent.theme.get_style_attr("SLabel:normal")
        self.update_theme(self.normal)

    def _draw_border(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        """SLabel don't need to draw border"""
        return