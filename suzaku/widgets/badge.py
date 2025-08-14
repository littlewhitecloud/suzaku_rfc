import typing

import skia

from ..resource import SColor
from .textframe import STextFrame, tpos


class SBadge(STextFrame):
    def __init__(
        self,
        *args,
        name: str = "SBadge",
        size: tuple[tpos, tpos] = (105, 35),
        text: typing.Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, widgetname=name, size=size, text=text, **kwargs)

        self.radius = 16
        self.bg = SColor([5, 105, 200, 255]).color
        self.bd = skia.ColorTRANSPARENT
