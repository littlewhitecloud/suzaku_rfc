from .widget import SWidget
import typing
import skia


class SImage(SWidget):
    def __init__(
        self,
        *args,
        widgetname: str = "SImage",
        image: str,
        size: typing.Tuple[int, int] = (800, 600),
        _id: typing.Optional[str] = None,
        **kwargs
    ):
        super().__init__(*args, widgetname=widgetname, size=size,**kwargs)
        self.image = skia.Image.open(image)
        self.takefocus = False

        self.resize = (self.image.width, self.image.height) != size

    def draw(self, canvas: skia.Surface):
        """Call widget default draw function
        
        :param canvas: skia Surface
        """
        self._draw(canvas)

    def _draw(self, canvas: skia.Surface):
        """SImage default draw function
        
        :param canvas: skia Surface
        """
        if not self.resize:
            canvas.drawImage(self.image, self.x, self.y)
            return
        src_rect = skia.Rect(self.x, self.y, self.x + self.image.width(),self.y + self.image.height())
        dst_rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)
        canvas.drawImageRect(self.image, src_rect, dst_rect, skia.SamplingOptions())

    def _on_theme_update(self) -> None:
        ...

    def update_theme(self) -> None:
        ...
