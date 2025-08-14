import skia
import typing

from .textframe import STextFrame, tpos


class SLabel(STextFrame):
    def __init__(
        self,
        *args,
        name: str = "SButton",
        size: tuple[tpos, tpos] = (0, 0),
        text: typing.Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, widgetname=name, size=size, text=text, shadow=False, **kwargs)

        self.bg = self.bd = skia.ColorTRANSPARENT
