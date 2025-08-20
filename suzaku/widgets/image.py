import typing

import skia

from .widget import SWidget


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
        super().__init__(*args, widgetname=widgetname, size=size, **kwargs)
        self.image = skia.Image.open(image)
        self.texture = None

        self.takefocus = False

        self._image_sampling = skia.SamplingOptions()

        self.resize = (self.image.width, self.image.height) != size
        # del self.iamge

    def make_image_to_texture(self) -> None:
        self.image.convert(skia.ColorType.kARGB_4444_ColorType)
        self.texture = self.image.makeTextureImage(self.parent._context)
        del self.image

    def draw(self, canvas: skia.Surface):
        """Call widget default draw function

        :param canvas: skia Surface
        """
        self._draw(canvas)

    def _draw(self, canvas: skia.Surface):
        """SImage default draw function

        :param canvas: skia Surface
        """
        if not self.texture:
            self.make_image_to_texture()
        if self.resize:
            # TODO: set src_rect self attr
            src_rect = skia.Rect(
                self.x,
                self.y,
                self.x + self.texture.width(),
                self.y + self.texture.height(),
            )
            dst_rect = skia.Rect(
                self.x, self.y, self.x + self.width, self.y + self.height
            )
            canvas.drawImageRect(self.texture, src_rect, dst_rect, self._image_sampling)
        else:
            canvas.drawImage(self.texture, self.x, self.y)

    def _on_theme_update(self) -> None: ...

    def update_theme(self) -> None: ...
