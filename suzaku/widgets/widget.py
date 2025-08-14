import typing

import skia

from .. import Window
from ..event import SEventHandler

tpos = int | float


class SWidget(SEventHandler):

    _instances = 0

    def __init__(
        self,
        widgetname: str,
        parent: "Window",
        size: tuple[tpos, tpos] = (200, 40),
        x: tpos = 100,
        y: tpos = 100,
        _id: typing.Optional[str] = None,
    ) -> None:
        super().__init__()
        self._name = widgetname
        self.parent = parent  # TODO: check parent

        # data region
        self.x: tpos = x
        self.y: tpos = y
        self.width: tpos = size[0]
        self.height: tpos = size[1]
        self.id = _id if _id else self._name + "." + str(self._instances)
        self._instances += 1

        self.padx: tpos = 0
        self.pady: tpos = 0

        self.radius: int = 0
        # end region

        self.parent.add_children(self)

    def _draw_shadow(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        _shadow_paint = skia.Paint(
            AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style, Color=skia.ColorGRAY
        )
        _shadow_paint.setImageFilter(skia.ImageFilters.Blur(10, 10))
        canvas.drawRoundRect(rect, self.radius, self.radius, _shadow_paint)

    def _draw(self) -> None: ...

    def draw(self, canvas: skia.Surface) -> None:
        """Execute the widget rendering and subwidget rendering

        :param canvas:
        """
        rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)

        self._draw(canvas, rect)
        # if the widget is like frame or something else and have children
        # then check if it have `draw_children` function and execute it
        # TODO: implement draw_children in other widgets
        if hasattr(self, "draw_children"):
            self.draw_children(canvas)
