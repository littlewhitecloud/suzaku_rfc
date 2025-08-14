import typing

import skia

from ..resource import SColor, default_font
from .widget import SWidget, tpos

# [112, 110, 170]


class STextFrame(SWidget):
    def __init__(
        self,
        *args,
        widgetname: str = "STextFrame",
        size: tuple[tpos, tpos] = (105, 35),
        shadow: bool = True,
        text: typing.Optional[str] = None,
        **kwargs
    ):
        super().__init__(*args, widgetname=widgetname, size=size, **kwargs)

        self.text: str = text
        self.radius = 8
        self.shadow = shadow

        # TODO: to fixed
        self.bg = SColor([33, 33, 33, 235]).color
        self.bd = SColor([43, 43, 43, 150]).color

    def _draw_text(self, canvas: skia.Surface) -> None:
        """Draw text

        :param canvas: skia Surface
        """
        paint = skia.Paint(
            AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kFill_Style
        )
        text_width = default_font.measureText(self.text)
        metrics = default_font.getMetrics()

        draw_x = self.x + self.width / 2 - text_width / 2
        draw_y = self.y + self.height / 2 - (metrics.fAscent + metrics.fDescent) / 2

        canvas.drawSimpleText(self.text, draw_x, draw_y, default_font, paint)

    def _draw(self, canvas: skia.Surface) -> None:
        """Default draw function

        :param canvas: skia Surface
        :param rect: the rect of the widget
        """

        rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)
        _frame_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style)
        _border_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style)

        _frame_paint.setColor(self.bg)
        _frame_paint.setStrokeWidth(2)

        _border_paint.setColor(self.bd)
        _border_paint.setStrokeWidth(2)

        if self.shadow:
            self._draw_shadow(canvas, rect)
        
        points=[
            (self.x, self.y),
            (self.width, self.height)
        ]
        #colors=[SColor([5, 105, 200, 255]).color ,SColor([112, 110, 170]).color, SColor([128, 155, 209]).color]
        #self.gran = skia.GradientShader.MakeLinear(points, colors)
        #_frame_paint.setShader(self.gran)
        canvas.drawRoundRect(rect, self.radius, self.radius, _frame_paint)
        canvas.drawRoundRect(rect, self.radius, self.radius, _border_paint)

        self._draw_text(canvas)  # layer

    def draw(self, canvas: skia.Surface) -> None:
        """Call draw funciton

        :param canvas: skia Surface
        """
        # TODO: improve the docstring
        self._draw(canvas)
