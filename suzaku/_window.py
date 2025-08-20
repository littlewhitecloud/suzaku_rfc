import contextlib
import gc
import typing

import glfw
import skia

from .after import SAfter
from .event import SEventHandler


class Window(SEventHandler, SAfter):

    _instances = 0

    def __init__(
        self,
        app: typing.Any,
        title: str,
        size: typing.Tuple[int],
        _name: str = "Window",
        _id=None,
    ) -> None:
        """Initialize the window

        :param title: the title of the window
        :param size: the size of the window
        :param:
        """
        SEventHandler.__init__(self)
        SAfter.__init__(self)

        # region info
        self.window: typing.Any = None
        self.application = app

        self.alive: bool = False
        self.name = _name
        self.id: str = _id if _id else self.name + "." + str(Window._instances)
        Window._instances += 1
        # end region

        # region winfo
        self.title: str = title
        (self.width, self.height) = size
        # window & mouse pos
        self.x = self.y = 0
        self.root_x = self.root_y = 0
        self.mouse_x = self.mouse_y = 0
        self.mouse_rootx = self.mouse_rooty = 0

        self.cursor: str = "arrow"
        self.focus: bool = True

        self._context = "None"
        self._backend_render_target = None
        self._make_srgb = skia.ColorSpace.MakeSRGB()
        # end region

        self.children: typing.List["SWidget"] = []  # noqa: F821

    def _draw(self, surface: typing.Any) -> None:
        """Draw both window and the children widgets"""
        # draw the window's children widgets
        for child in self.children:
            child.draw(surface)

    def create_window(self) -> None:
        """Create the glfw window"""
        self.window = glfw.create_window(
            self.width, self.height, self.title, None, None
        )

        (self.root_x, self.root_y) = glfw.get_window_pos(self.window)

        if not self.window and not glfw.window_should_close(self.window):
            raise RuntimeError("Failed to create a glfw window instance")

        self.alive = True

    def get_context(self) -> None:
        # make context
        self._context = skia.GrDirectContext.MakeGL()
        self._context.setResourceCacheLimit(16 * 1024 * 1024)

    @contextlib.contextmanager
    def get_surface(self) -> typing.Any:
        """Get/Create the skia surface"""
        # check if the window is vaild now
        if not glfw.get_current_context() or glfw.window_should_close(self.window):
            yield None
            return

        try:
            # make backend
            (FB_WIDTH, FB_HEIGHT) = glfw.get_framebuffer_size(self.window)
            if not (
                self._backend_render_target
                and self.width == FB_WIDTH
                and self.height == FB_HEIGHT
            ):
                self.width = FB_WIDTH
                self.height = FB_HEIGHT
                # GL_RGBA8 = 0x8058
                self._backend_render_target = skia.GrBackendRenderTarget(
                    FB_WIDTH, FB_HEIGHT, 0, 0, skia.GrGLFramebufferInfo(0, 0x8058)
                )
            # make surface
            surface = skia.Surface.MakeFromBackendRenderTarget(
                self._context,
                self._backend_render_target,
                skia.kBottomLeft_GrSurfaceOrigin,
                skia.kRGBA_8888_ColorType,
                self._make_srgb,
            )
            del FB_HEIGHT, FB_WIDTH
            # assert surface
            if surface is None:
                raise RuntimeError("Failed to create a skia surface")
            yield surface
            # del surface
        finally:
            pass
            # self._context.freeGpuResources()  # noqa: F821
            # self._context.releaseResourcesAndAbandonContext()  # noqa: F821
            # print()

    def destroy_window(self) -> None:
        """Destory the window"""
        # destory window
        self.alive = False

        if glfw.get_current_context() is None:
            glfw.make_context_current(self.window)

        if self.children:
            for _ in self.children:
                del _

        if self._context:
            self._context.freeGpuResources()
            self._context.releaseResourcesAndAbandonContext()
            self._context = None

        if self.window:
            glfw.destroy_window(self.window)
            self.window = None

        gc.collect()

    destroy = destroy_window
