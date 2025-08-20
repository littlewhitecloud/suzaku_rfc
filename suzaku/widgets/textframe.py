import typing

import skia

from ..resource import SColor, default_font
from .widget import SWidget, tpos


class STextFrame(SWidget):
    def __init__(
        self,
        *args,
        widgetname: str = "STextframe",
        size: tuple[tpos, tpos] = (105, 35),
        text: typing.Optional[str] = None,
        **kwargs
    ):
        super().__init__(*args, widgetname=widgetname, size=size, **kwargs)
        self.text: str = text

        # draw region
        self._border_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style)
        self._border_paint.setStrokeWidth(2)
        self._frame_paint = skia.Paint(
            AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style
        )
        self._frame_paint.setStrokeWidth(2)
        self._text_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style)
        self._text_metrics = default_font.getMetrics()

        self.gradient = None
        # end region

    def _draw_text(self, canvas: skia.Surface) -> None:
        """Draw text

        :param canvas: skia Surface
        """
        self._text_paint.setColor(self.fg)

        text_width = default_font.measureText(self.text)

        self._text_draw_x = self.x + self.width / 2 - text_width / 2
        self._text_draw_y = (
            self.y
            + self.height / 2
            - (self._text_metrics.fAscent + self._text_metrics.fDescent) / 2
        )

        canvas.drawSimpleText(
            self.text,
            self._text_draw_x,
            self._text_draw_y,
            default_font,
            self._text_paint,
        )

    def _draw_border(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        """Draw border

        :param canvas: skia Surface
        :param rect: the widget rect
        """
        if not self.border:
            return
        self._border_paint.setColor(self.bd)

        canvas.drawRoundRect(rect, self.radius, self.radius, self._border_paint)

    def _get_shadow(self) -> None:
        """Get shadow"""
        self.points = [(self.x, self.y), (self.x + self.width, self.y + self.height)]
        self.colors = [
            SColor([5, 105, 200, 255]).color,
            SColor([110, 135, 185]).color,
            SColor([130, 65, 165]).color,
        ]
        self.gradient = skia.GradientShader.MakeLinear(self.points, self.colors)

    def _draw(self, canvas: skia.Surface) -> None:
        """Default draw function

        :param canvas: skia Surface
        :param rect: the widget rect
        """
        self._frame_paint.setColor(self.bg)
        if not self.gradient:
            self._get_shadow()
        self._shadow_paint.setShader(self.gradient)
        self._border_paint.setShader(self.gradient)

        self.rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)
        if self.shadow:
            self._draw_shadow(canvas, self.rect)

        canvas.drawRoundRect(self.rect, self.radius, self.radius, self._frame_paint)
        self._draw_border(canvas, self.rect)
        self._draw_text(canvas)  # layer

    def draw(self, canvas: skia.Surface) -> None:
        """Call default draw funciton

        :param canvas: skia Surface
        """
        self._draw(canvas)
