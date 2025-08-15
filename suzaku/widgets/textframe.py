import typing
from functools import partial

import skia

from ..resource import SColor, default_font
from .widget import SWidget, tpos

# [112, 110, 170]


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
        self.rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)
        self._border_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style)
        self._border_paint.setStrokeWidth(2)
        self._frame_paint = skia.Paint(
            AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style
        )
        self._frame_paint.setStrokeWidth(2)
        self._text_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style)
        self._text_metrics = default_font.getMetrics()
        # end region

    def _draw_text(self, canvas: skia.Surface) -> None:
        """Draw text

        :param canvas: skia Surface
        """
        self._text_paint.setColor(self.fg)

        text_width = default_font.measureText(self.text)

        draw_x = self.x + self.width / 2 - text_width / 2
        draw_y = (
            self.y
            + self.height / 2
            - (self._text_metrics.fAscent + self._text_metrics.fDescent) / 2
        )

        canvas.drawSimpleText(self.text, draw_x, draw_y, default_font, self._text_paint)

    def _draw_border(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        """Draw border

        :param canvas: skia Surface
        :param rect: the widget rect
        """
        if not self.border:
            return
        self._border_paint.setColor(self.bd)

        canvas.drawRoundRect(rect, self.radius, self.radius, self._border_paint)

    def _draw(self, canvas: skia.Surface) -> None:
        """Default draw function

        :param canvas: skia Surface
        :param rect: the widget rect
        """

        self._frame_paint.setColor(self.bg)
        # points=[
        #     (self.x, self.y),
        #     (self.width, self.height)
        # ]
        # colors=[SColor([5, 105, 200, 255]).color ,SColor([112, 110, 170]).color, SColor([128, 155, 209]).color]
        # self.gran = skia.GradientShader.MakeLinear(points, colors)
        # _frame_paint.setShader(self.gran)
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
