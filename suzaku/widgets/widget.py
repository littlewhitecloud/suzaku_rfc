import typing

import skia

from .. import Window
from ..container import SLayoutManager
from ..event import SEventHandler

tpos = int | float


class SWidget(SEventHandler, SLayoutManager):

    _instances = 0

    def __init__(
        self,
        widgetname: str,
        parent: "SWindow",
        size: tuple[tpos, tpos] = (200, 40),
        x: tpos = 100,
        y: tpos = 100,
        _id: typing.Optional[str] = None,
    ):
        SEventHandler.__init__(self)
        SLayoutManager.__init__(self)

        self._name = widgetname
        self.parent = parent  # TODO: check parent

        # data region
        self.x: tpos = x
        self.y: tpos = y
        self.width: tpos = size[0]
        self.height: tpos = size[1]
        self.id = _id if _id else self._name + "." + str(self._instances)
        self._instances += 1

        self.radius: int = 0
        # end region

        # draw region
        self.rect = None
        self._shadow_paint = skia.Paint(
            AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style, Color=skia.ColorGRAY
        )
        self._shadow_paint.setImageFilter(skia.ImageFilters.Blur(10, 10))
        # end region

        self.parent.add_children(self)

        return self

    def update_layout(self):
        for k, v in self.layoutconfig.items():
            setattr(self, k, v)

    def update_theme(self, theme_attr: dict) -> None:
        """Update theme attr from dict and register them

        :param theme_attr: the dict to register
        """
        # check if theme_attr is None for some reason
        # or just init the widget
        if not isinstance(theme_attr, dict):
            theme_attr = self.normal
        # register
        for k, v in theme_attr.items():
            setattr(self, k, v)

    def _on_theme_update(self, *args, **kwargs) -> None:
        """Handle parent window's theme update"""
        # first time init or get updated
        self.basic = self.parent.theme.get_style_attr(f"{self._name}:basic")
        self.normal = self.parent.theme.get_style_attr(f"{self._name}:normal")
        # TODO: avoid use []
        if self.basic["takefocus"]:
            self.focused = self.parent.theme.get_style_attr(f"{self._name}:focused")
        else:
            self.focused = self.normal  # TODO: improve it

        # register
        for _ in [self.basic, self.normal]:
            self.update_theme(_)

    def _draw_shadow(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        canvas.drawRoundRect(rect, self.radius, self.radius, self._shadow_paint)

    def _draw(self) -> None: ...

    def draw(self, canvas: skia.Surface) -> None:
        """Execute the widget rendering and subwidget rendering

        :param canvas:
        """
        if not self.rect:
            self.rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)

        self._draw(canvas, self.rect)
        # if the widget is like frame or something else and have children
        # then check if it have `draw_children` function and execute it
        # TODO: implement draw_children in other widgets
        if hasattr(self, "draw_children"):
            self.draw_children(canvas)
