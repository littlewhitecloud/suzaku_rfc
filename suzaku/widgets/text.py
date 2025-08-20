import typing

import skia

from ..resource import default_font
from .widget import SWidget, tpos


class SText(SWidget):

    _instances = 0

    def __init__(
        self,
        *args,
        name: str = "SButton",
        size: tuple[tpos, tpos] = (105, 35),
        text: typing.Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, widgetname=name, size=size, **kwargs)

        self.id = self._name + "." + str(self._instances)
        self._instances += 1

        # draw region
        self._border_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style)
        self._border_paint.setStrokeWidth(2)
        self._frame_paint = skia.Paint(
            AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style
        )
        self._frame_paint.setColor(self.bg)
        self._frame_paint.setStrokeWidth(2)
        self._text_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style)
        self._text_metrics = default_font.getMetrics()
        self._text_paint.setColor(self.fg)
        # end region

    def _draw_border(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        """Draw border

        :param canvas: skia Surface
        :param rect: the widget rect
        """
        if not self.border:
            return
        self._border_paint.setColor(self.bd)

        canvas.drawRoundRect(rect, self.radius, self.radius, self._border_paint)

    def _draw_cursor(self, canvas: skia.Surface) -> None:
        if not self.focused:
            return
        canvas.drawLine(
            x0=self.x,
            y0=self.y + self._text_metrics.fAscent,
            x1=self.x,
            y1=self.y + self._text_metrics.fDescent,
            paint=self._text_paint,
        )

    def _draw(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        """..."""
        canvas.drawRoundRect(rect, self.radius, self.radius, self._frame_paint)
        self._draw_border(canvas, rect)
        self._draw_cursor(canvas)

    def draw(self, canvas: skia.Surface):
        """..."""
        self.rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)

        self._draw(canvas, self.rect)
